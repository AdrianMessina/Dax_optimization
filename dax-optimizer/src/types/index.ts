export type DaxObjectType = 'measure' | 'calculated-column' | 'calculated-table';

export interface DaxAnalysisResult {
  code: string;
  objectType: DaxObjectType;
  issues: Issue[];
  suggestions: Suggestion[];
  score: number; // 0-100
  metrics: PerformanceMetrics;
}

export interface Issue {
  id: string;
  severity: 'critical' | 'warning' | 'info';
  category: string;
  title: string;
  description: string;
  line?: number;
  column?: number;
  snippet?: string;
  learnMore?: string;
}

export interface Suggestion {
  id: string;
  title: string;
  description: string;
  originalCode: string;
  suggestedCode: string;
  impact: 'high' | 'medium' | 'low';
  reason: string;
}

export interface PerformanceMetrics {
  complexity: number; // 0-100
  nestedIterators: number;
  contextTransitions: number;
  variablesUsed: number;
  functionCount: number;
  estimatedImpact: 'high' | 'medium' | 'low';
}

export interface ParsedDaxExpression {
  raw: string;
  objectType: DaxObjectType;
  name?: string;
  functions: FunctionCall[];
  tables: string[];
  columns: string[];
  measures: string[];
  hasVariables: boolean;
  variables: Variable[];
}

export interface FunctionCall {
  name: string;
  line: number;
  column: number;
  nested: boolean;
  parent?: string;
}

export interface Variable {
  name: string;
  usageCount: number;
}
