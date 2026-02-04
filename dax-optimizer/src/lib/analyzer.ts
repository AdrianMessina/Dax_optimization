import { ParsedDaxExpression, Issue, PerformanceMetrics } from '../types';
import { calculateComplexity } from './daxParser';

export function analyzeDAX(parsed: ParsedDaxExpression): { issues: Issue[]; metrics: PerformanceMetrics } {
  const issues: Issue[] = [];

  // Run all anti-pattern checks
  checkNestedIterators(parsed, issues);
  checkFilterWithoutKeepFilters(parsed, issues);
  checkMissingVariables(parsed, issues);
  checkCalculateNesting(parsed, issues);
  checkAllInFilter(parsed, issues);
  checkExpensiveFunctions(parsed, issues);
  checkContextTransitions(parsed, issues);
  checkCalculatedColumnsInMeasures(parsed, issues);
  checkRepeatedExpressions(parsed, issues);

  // Calculate metrics
  const metrics = calculateMetrics(parsed);

  return { issues, metrics };
}

function checkNestedIterators(parsed: ParsedDaxExpression, issues: Issue[]): void {
  const iterators = ['SUMX', 'AVERAGEX', 'COUNTX', 'COUNTAX', 'MINX', 'MAXX', 'CONCATENATEX', 'RANKX'];

  iterators.forEach(outerIterator => {
    const outerPattern = new RegExp(`${outerIterator}\\s*\\([^)]*`, 'i');
    const outerMatch = parsed.raw.match(outerPattern);

    if (outerMatch) {
      iterators.forEach(innerIterator => {
        const innerPattern = new RegExp(`${outerIterator}\\s*\\([^)]*${innerIterator}\\s*\\(`, 'i');
        if (innerPattern.test(parsed.raw)) {
          issues.push({
            id: 'nested-iterators',
            severity: 'critical',
            category: 'Performance',
            title: 'Iteradores anidados detectados',
            description: `Se detectó ${innerIterator} dentro de ${outerIterator}. Esto causa que cada fila de la tabla externa evalúe todas las filas de la tabla interna, resultando en complejidad O(n²) o mayor.`,
            snippet: outerMatch[0] + '...',
            learnMore: 'https://www.sqlbi.com/articles/optimizing-nested-iterators-in-dax/'
          });
        }
      });
    }
  });
}

function checkFilterWithoutKeepFilters(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // Check for FILTER inside CALCULATE without KEEPFILTERS
  const calculateWithFilter = /CALCULATE\s*\([^)]*FILTER\s*\(/gi;

  if (calculateWithFilter.test(parsed.raw) && !parsed.raw.toUpperCase().includes('KEEPFILTERS')) {
    issues.push({
      id: 'filter-without-keepfilters',
      severity: 'warning',
      category: 'Filter Context',
      title: 'FILTER en CALCULATE sin KEEPFILTERS',
      description: 'Usar FILTER directamente en CALCULATE puede sobrescribir filtros existentes. Considera usar KEEPFILTERS(FILTER(...)) para mantener el contexto de filtro existente.',
      learnMore: 'https://www.sqlbi.com/articles/using-keepfilters-in-dax/'
    });
  }
}

function checkMissingVariables(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // Check for repeated complex expressions
  const calculatePattern = /CALCULATE\s*\([^)]+\)/gi;
  const calculateMatches = parsed.raw.match(calculatePattern);

  if (calculateMatches && calculateMatches.length > 1 && parsed.variables.length === 0) {
    const repeatedExpressions = findRepeatedExpressions(calculateMatches);

    if (repeatedExpressions.length > 0) {
      issues.push({
        id: 'missing-variables',
        severity: 'warning',
        category: 'Code Quality',
        title: 'Expresiones repetidas sin variables',
        description: 'Se detectaron expresiones repetidas. Usar VAR para almacenar cálculos intermedios mejora la performance y legibilidad.',
        snippet: repeatedExpressions[0],
        learnMore: 'https://www.sqlbi.com/articles/using-variables-in-dax/'
      });
    }
  }

  // Check for complex expressions without variables
  if (parsed.functions.length > 5 && parsed.variables.length === 0) {
    issues.push({
      id: 'no-variables-complex',
      severity: 'info',
      category: 'Code Quality',
      title: 'Código complejo sin variables',
      description: 'Tu código tiene múltiples funciones pero no usa variables. Considera usar VAR para mejorar legibilidad y potencialmente performance.',
      learnMore: 'https://www.sqlbi.com/articles/using-variables-in-dax/'
    });
  }
}

function checkCalculateNesting(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // Check for nested CALCULATE calls
  const nestedCalculate = /CALCULATE\s*\([^)]*CALCULATE\s*\(/i;

  if (nestedCalculate.test(parsed.raw)) {
    issues.push({
      id: 'nested-calculate',
      severity: 'warning',
      category: 'Context Transition',
      title: 'CALCULATE anidado detectado',
      description: 'CALCULATE anidado causa múltiples transiciones de contexto innecesarias. Considera combinar los filtros en un solo CALCULATE.',
      learnMore: 'https://www.sqlbi.com/articles/understanding-context-transition/'
    });
  }
}

function checkAllInFilter(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // Check for ALL() used directly in FILTER
  const allInFilter = /FILTER\s*\(\s*ALL\s*\(/i;

  if (allInFilter.test(parsed.raw)) {
    issues.push({
      id: 'all-in-filter',
      severity: 'critical',
      category: 'Performance',
      title: 'ALL() usado en FILTER sobre tabla completa',
      description: 'FILTER(ALL(Tabla), ...) itera sobre todas las filas sin aprovechar índices. Considera usar CALCULATE con filtros o FILTER solo sobre columnas específicas.',
      learnMore: 'https://www.sqlbi.com/articles/best-practices-using-filter-and-all/'
    });
  }
}

function checkExpensiveFunctions(parsed: ParsedDaxExpression, issues: Issue[]): void {
  const expensiveFunctions = [
    { name: 'CROSSJOIN', reason: 'genera producto cartesiano de tablas' },
    { name: 'GENERATE', reason: 'itera y genera filas para cada fila de entrada' },
    { name: 'SUMMARIZE', reason: 'puede ser reemplazado por SUMMARIZECOLUMNS (más eficiente)' },
    { name: 'LOOKUPVALUE', reason: 'hace búsquedas lineales, considera usar RELATED si hay relación' }
  ];

  expensiveFunctions.forEach(({ name, reason }) => {
    const pattern = new RegExp(`\\b${name}\\s*\\(`, 'i');
    if (pattern.test(parsed.raw)) {
      issues.push({
        id: `expensive-${name.toLowerCase()}`,
        severity: 'warning',
        category: 'Performance',
        title: `Función costosa: ${name}`,
        description: `${name} ${reason}. Evalúa si hay una alternativa más eficiente.`,
        learnMore: `https://www.sqlbi.com/articles/optimizing-dax-expressions/`
      });
    }
  });
}

function checkContextTransitions(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // In calculated columns, using measures causes context transition
  if (parsed.objectType === 'calculated-column') {
    const hasMeasureReference = parsed.measures.length > 0;

    if (hasMeasureReference) {
      issues.push({
        id: 'measure-in-calculated-column',
        severity: 'critical',
        category: 'Context Transition',
        title: 'Medida usada en columna calculada',
        description: 'Usar medidas en columnas calculadas causa transición de contexto en cada fila, lo cual es muy costoso. Considera reescribir la lógica usando funciones de columna calculada.',
        learnMore: 'https://www.sqlbi.com/articles/understanding-context-transition/'
      });
    }
  }
}

function checkCalculatedColumnsInMeasures(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // Detect patterns that suggest calculated columns usage
  if (parsed.objectType === 'measure') {
    const hasEarlier = /\bEARLIER\s*\(/i.test(parsed.raw);

    if (hasEarlier) {
      issues.push({
        id: 'earlier-in-measure',
        severity: 'warning',
        category: 'Code Quality',
        title: 'EARLIER detectado en medida',
        description: 'EARLIER se usa típicamente en columnas calculadas. Si estás intentando usar lógica de columna calculada en una medida, considera crear la columna calculada por separado o usar variables.',
        learnMore: 'https://www.sqlbi.com/articles/row-context-and-filter-context-in-dax/'
      });
    }
  }
}

function checkRepeatedExpressions(parsed: ParsedDaxExpression, issues: Issue[]): void {
  // Check for measure references used multiple times
  const measureCounts = new Map<string, number>();

  parsed.measures.forEach(measure => {
    const pattern = new RegExp(`\\[${measure}\\]`, 'g');
    const matches = parsed.raw.match(pattern);
    if (matches && matches.length > 2) {
      measureCounts.set(measure, matches.length);
    }
  });

  if (measureCounts.size > 0 && parsed.variables.length === 0) {
    const mostRepeated = Array.from(measureCounts.entries())
      .sort((a, b) => b[1] - a[1])[0];

    issues.push({
      id: 'repeated-measure-reference',
      severity: 'info',
      category: 'Code Quality',
      title: 'Referencia a medida repetida',
      description: `La medida [${mostRepeated[0]}] se usa ${mostRepeated[1]} veces. Considera almacenarla en una variable para evaluar solo una vez.`,
      learnMore: 'https://www.sqlbi.com/articles/using-variables-in-dax/'
    });
  }
}

function findRepeatedExpressions(expressions: string[]): string[] {
  const counts = new Map<string, number>();

  expressions.forEach(expr => {
    const normalized = expr.replace(/\s+/g, ' ').trim();
    counts.set(normalized, (counts.get(normalized) || 0) + 1);
  });

  return Array.from(counts.entries())
    .filter(([_, count]) => count > 1)
    .map(([expr]) => expr);
}

function calculateMetrics(parsed: ParsedDaxExpression): PerformanceMetrics {
  const complexity = calculateComplexity(parsed);

  const nestedIterators = parsed.functions.filter(f => f.nested).length;

  const contextTransitionFuncs = ['CALCULATE', 'CALCULATETABLE'];
  const contextTransitions = parsed.functions.filter(f =>
    contextTransitionFuncs.includes(f.name)
  ).length;

  let estimatedImpact: 'high' | 'medium' | 'low' = 'low';
  if (complexity > 60 || nestedIterators > 0) {
    estimatedImpact = 'high';
  } else if (complexity > 30 || contextTransitions > 2) {
    estimatedImpact = 'medium';
  }

  return {
    complexity,
    nestedIterators,
    contextTransitions,
    variablesUsed: parsed.variables.length,
    functionCount: parsed.functions.length,
    estimatedImpact
  };
}
