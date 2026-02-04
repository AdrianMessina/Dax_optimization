import { DaxAnalysisResult } from '../types';
import { parseDaxCode } from './daxParser';
import { analyzeDAX } from './analyzer';
import { generateSuggestions, calculateScore } from './suggestions';

export function analyzeDaxCode(code: string): DaxAnalysisResult {
  // Parse the DAX code
  const parsed = parseDaxCode(code);

  // Analyze for issues
  const { issues, metrics } = analyzeDAX(parsed);

  // Generate suggestions
  const suggestions = generateSuggestions(parsed, issues);

  // Calculate overall score
  const score = calculateScore(parsed, issues);

  return {
    code,
    objectType: parsed.objectType,
    issues,
    suggestions,
    score,
    metrics
  };
}

export * from '../types';
