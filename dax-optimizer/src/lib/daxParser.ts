import { DaxObjectType, ParsedDaxExpression, FunctionCall, Variable } from '../types';

// Common DAX functions
const DAX_FUNCTIONS = [
  'CALCULATE', 'FILTER', 'ALL', 'ALLSELECTED', 'ALLEXCEPT', 'VALUES', 'DISTINCT',
  'SUM', 'SUMX', 'AVERAGE', 'AVERAGEX', 'COUNT', 'COUNTX', 'COUNTA', 'COUNTAX',
  'MIN', 'MINX', 'MAX', 'MAXX', 'CONCATENATEX', 'RANKX',
  'EARLIER', 'EARLIEST', 'RELATED', 'RELATEDTABLE', 'USERELATIONSHIP',
  'IF', 'SWITCH', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
  'BLANK', 'ISBLANK', 'IFERROR', 'ISERROR',
  'VAR', 'RETURN',
  'SUMMARIZE', 'SUMMARIZECOLUMNS', 'ADDCOLUMNS', 'SELECTCOLUMNS',
  'CROSSJOIN', 'GENERATE', 'GENERATEALL', 'NATURALINNERJOIN', 'NATURALLEFTOUTERJOIN',
  'KEEPFILTERS', 'REMOVEFILTERS', 'SELECTEDVALUE',
  'DIVIDE', 'FORMAT', 'CONCATENATE',
  'CALENDAR', 'CALENDARAUTO', 'DATE', 'DATEVALUE',
  'TOTALYTD', 'TOTALQTD', 'TOTALMTD', 'DATEADD', 'DATESYTD',
  'HASONEVALUE', 'HASONEFILTER', 'ISCROSSFILTERED', 'ISFILTERED',
  'LOOKUPVALUE', 'TREATAS', 'SUBSTITUTEWITHINDEX'
];

const ITERATOR_FUNCTIONS = [
  'SUMX', 'AVERAGEX', 'COUNTX', 'COUNTAX', 'MINX', 'MAXX',
  'CONCATENATEX', 'RANKX', 'PRODUCTX', 'MEDIANX', 'PERCENTILX.INC', 'PERCENTILX.EXC'
];

export function parseDaxCode(code: string): ParsedDaxExpression {
  const trimmedCode = code.trim();

  // Detect object type
  const objectType = detectObjectType(trimmedCode);

  // Extract name if present
  const name = extractName(trimmedCode, objectType);

  // Extract variables
  const variables = extractVariables(trimmedCode);

  // Extract functions with position
  const functions = extractFunctions(trimmedCode);

  // Extract table and column references
  const { tables, columns } = extractTableColumnReferences(trimmedCode);

  // Extract measure references
  const measures = extractMeasureReferences(trimmedCode);

  return {
    raw: code,
    objectType,
    name,
    functions,
    tables,
    columns,
    measures,
    hasVariables: variables.length > 0,
    variables
  };
}

function detectObjectType(code: string): DaxObjectType {
  // Calculated table: usually starts with table name = SOME_TABLE_FUNCTION
  // and doesn't have aggregation functions
  const tablePattern = /^\s*[\w\s]+\s*=\s*(FILTER|SUMMARIZE|ADDCOLUMNS|SELECTCOLUMNS|CROSSJOIN|CALENDAR|CALENDARAUTO|GENERATE|DISTINCT|VALUES|ALL)/i;

  // Calculated column: often uses EARLIER or RELATED, or row context functions
  const columnIndicators = /\b(EARLIER|EARLIEST|PATH|PATHITEM)\b/i;

  if (tablePattern.test(code)) {
    return 'calculated-table';
  }

  if (columnIndicators.test(code)) {
    return 'calculated-column';
  }

  // Default to measure (most common case)
  return 'measure';
}

function extractName(code: string, objectType: DaxObjectType): string | undefined {
  // Try to extract name from pattern: Name = ...
  const namePattern = /^\s*(\[?[\w\s]+\]?)\s*=/;
  const match = code.match(namePattern);
  return match ? match[1].trim().replace(/[\[\]]/g, '') : undefined;
}

function extractVariables(code: string): Variable[] {
  const varPattern = /\bVAR\s+([\w_]+)\s*=/gi;
  const variables: Map<string, number> = new Map();

  let match;
  while ((match = varPattern.exec(code)) !== null) {
    const varName = match[1];
    variables.set(varName, 0);
  }

  // Count usages (excluding the declaration)
  variables.forEach((_, varName) => {
    const usagePattern = new RegExp(`\\b${varName}\\b`, 'g');
    const matches = code.match(usagePattern);
    // -1 because we don't count the declaration
    variables.set(varName, (matches?.length || 1) - 1);
  });

  return Array.from(variables.entries()).map(([name, usageCount]) => ({
    name,
    usageCount
  }));
}

function extractFunctions(code: string): FunctionCall[] {
  const functions: FunctionCall[] = [];
  const lines = code.split('\n');

  lines.forEach((line, lineIndex) => {
    DAX_FUNCTIONS.forEach(funcName => {
      const pattern = new RegExp(`\\b${funcName}\\s*\\(`, 'gi');
      let match;

      while ((match = pattern.exec(line)) !== null) {
        functions.push({
          name: funcName.toUpperCase(),
          line: lineIndex + 1,
          column: match.index,
          nested: false, // Will calculate this later
        });
      }
    });
  });

  // Detect nested iterators (simplified)
  functions.forEach(func => {
    if (ITERATOR_FUNCTIONS.includes(func.name)) {
      const funcLine = lines[func.line - 1];
      const afterFunc = funcLine.substring(func.column);

      // Check if there's another iterator inside (very simplified)
      const hasNestedIterator = ITERATOR_FUNCTIONS.some(iterFunc =>
        afterFunc.includes(`${iterFunc}(`)
      );

      if (hasNestedIterator) {
        func.nested = true;
      }
    }
  });

  return functions;
}

function extractTableColumnReferences(code: string): { tables: string[]; columns: string[] } {
  const tables = new Set<string>();
  const columns = new Set<string>();

  // Pattern for Table[Column] or 'Table'[Column]
  const tableColumnPattern = /['"]?(\w+)['"]?\[(\w+)\]/g;

  let match;
  while ((match = tableColumnPattern.exec(code)) !== null) {
    tables.add(match[1]);
    columns.add(`${match[1]}[${match[2]}]`);
  }

  return {
    tables: Array.from(tables),
    columns: Array.from(columns)
  };
}

function extractMeasureReferences(code: string): string[] {
  const measures = new Set<string>();

  // Pattern for [Measure Name]
  const measurePattern = /\[([^\]]+)\]/g;

  let match;
  while ((match = measurePattern.exec(code)) !== null) {
    // Exclude if it's part of Table[Column]
    const beforeBracket = code.substring(Math.max(0, match.index - 10), match.index);
    if (!beforeBracket.match(/['"]?\w+['"]?$/)) {
      measures.add(match[1]);
    }
  }

  return Array.from(measures);
}

export function calculateComplexity(parsed: ParsedDaxExpression): number {
  let complexity = 0;

  // Base complexity
  complexity += parsed.functions.length * 2;

  // Nested iterators add significant complexity
  const nestedIterators = parsed.functions.filter(f => f.nested).length;
  complexity += nestedIterators * 15;

  // CALCULATE adds context transition
  const calculateCount = parsed.functions.filter(f => f.name === 'CALCULATE').length;
  complexity += calculateCount * 5;

  // Variables reduce complexity
  complexity -= parsed.variables.length * 3;

  // Multiple table references add complexity
  complexity += parsed.tables.length * 2;

  // Normalize to 0-100
  return Math.min(100, Math.max(0, complexity));
}
