import { ParsedDaxExpression, Issue, Suggestion } from '../types';

export function generateSuggestions(
  parsed: ParsedDaxExpression,
  issues: Issue[]
): Suggestion[] {
  const suggestions: Suggestion[] = [];

  // Generate suggestions based on issues
  issues.forEach(issue => {
    switch (issue.id) {
      case 'nested-iterators':
        suggestions.push(generateNestedIteratorSuggestion(parsed));
        break;
      case 'filter-without-keepfilters':
        suggestions.push(generateKeepFiltersSuggestion(parsed));
        break;
      case 'missing-variables':
      case 'no-variables-complex':
        suggestions.push(generateVariableSuggestion(parsed));
        break;
      case 'nested-calculate':
        suggestions.push(generateFlattenCalculateSuggestion(parsed));
        break;
      case 'all-in-filter':
        suggestions.push(generateAllInFilterSuggestion(parsed));
        break;
    }
  });

  // Always suggest variable usage if expressions are repeated
  if (parsed.variables.length === 0 && parsed.functions.length > 3) {
    const varSuggestion = generateGenericVariableSuggestion(parsed);
    if (varSuggestion && !suggestions.find(s => s.id === 'add-variables')) {
      suggestions.push(varSuggestion);
    }
  }

  return suggestions;
}

function generateNestedIteratorSuggestion(parsed: ParsedDaxExpression): Suggestion {
  // Example transformation for nested SUMX
  const example = `-- ❌ Original (nested iterators):
SUMX(
    Tabla1,
    SUMX(
        FILTER(Tabla2, Tabla2[ID] = Tabla1[ID]),
        Tabla2[Valor]
    )
)

-- ✅ Optimizado (usando variables y relaciones):
SUMX(
    Tabla1,
    VAR TablaFiltrada =
        FILTER(Tabla2, Tabla2[ID] = Tabla1[ID])
    RETURN
        CALCULATE(SUM(Tabla2[Valor]), TablaFiltrada)
)

-- ✅ Mejor aún (si existe relación):
SUMX(
    Tabla1,
    CALCULATE(SUM(Tabla2[Valor]))
)`;

  return {
    id: 'optimize-nested-iterators',
    title: 'Eliminar iteradores anidados',
    description: 'Refactoriza para evitar iterar múltiples veces',
    originalCode: 'Patrón detectado: SUMX(..., SUMX(...))',
    suggestedCode: example,
    impact: 'high',
    reason: 'Reduce complejidad de O(n²) a O(n), mejorando drásticamente la performance en tablas grandes.'
  };
}

function generateKeepFiltersSuggestion(parsed: ParsedDaxExpression): Suggestion {
  return {
    id: 'add-keepfilters',
    title: 'Usar KEEPFILTERS para mantener contexto',
    description: 'Envuelve FILTER con KEEPFILTERS',
    originalCode: 'CALCULATE([Medida], FILTER(...))',
    suggestedCode: 'CALCULATE([Medida], KEEPFILTERS(FILTER(...)))',
    impact: 'medium',
    reason: 'KEEPFILTERS respeta los filtros existentes en lugar de sobrescribirlos, evitando resultados inesperados.'
  };
}

function generateVariableSuggestion(parsed: ParsedDaxExpression): Suggestion {
  // Find a repeated pattern to use as example
  let example = '';

  // Check if there are repeated CALCULATEs
  const calculateMatches = parsed.raw.match(/CALCULATE\s*\([^)]+\)/gi);
  if (calculateMatches && calculateMatches.length > 0) {
    const firstCalc = calculateMatches[0].length > 60
      ? calculateMatches[0].substring(0, 60) + '...'
      : calculateMatches[0];

    example = `-- ❌ Original:
${firstCalc}
... (usado múltiples veces) ...

-- ✅ Con variables:
VAR MiCalculo = ${firstCalc}
RETURN
    IF(MiCalculo > 0, MiCalculo, BLANK())`;
  } else {
    example = `-- ✅ Patrón recomendado:
VAR Ventas = SUM(Tabla[Ventas])
VAR Costos = SUM(Tabla[Costos])
VAR Margen = Ventas - Costos
RETURN
    DIVIDE(Margen, Ventas)`;
  }

  return {
    id: 'add-variables',
    title: 'Introducir variables (VAR)',
    description: 'Almacena cálculos intermedios en variables',
    originalCode: 'Expresiones repetidas o código sin variables',
    suggestedCode: example,
    impact: 'medium',
    reason: 'Las variables se evalúan una sola vez y se reutilizan, mejorando performance y legibilidad.'
  };
}

function generateFlattenCalculateSuggestion(parsed: ParsedDaxExpression): Suggestion {
  return {
    id: 'flatten-calculate',
    title: 'Aplanar CALCULATEs anidados',
    description: 'Combina múltiples CALCULATE en uno solo',
    originalCode: `CALCULATE(
    CALCULATE([Medida], Filtro1),
    Filtro2
)`,
    suggestedCode: `CALCULATE(
    [Medida],
    Filtro1,
    Filtro2
)`,
    impact: 'medium',
    reason: 'Elimina transiciones de contexto innecesarias, reduciendo overhead de evaluación.'
  };
}

function generateAllInFilterSuggestion(parsed: ParsedDaxExpression): Suggestion {
  return {
    id: 'optimize-all-filter',
    title: 'Optimizar uso de ALL en FILTER',
    description: 'Usa CALCULATE en lugar de FILTER(ALL(...))',
    originalCode: `FILTER(
    ALL(Tabla),
    Tabla[Columna] = Valor
)`,
    suggestedCode: `CALCULATE(
    VALUES(Tabla),
    Tabla[Columna] = Valor,
    REMOVEFILTERS(Tabla)
)

-- O mejor, si solo filtras una columna:
CALCULATETABLE(
    VALUES(Tabla),
    Tabla[Columna] = Valor,
    REMOVEFILTERS(Tabla)
)`,
    impact: 'high',
    reason: 'CALCULATE puede aprovechar índices y optimizaciones del motor, mientras que FILTER(ALL(...)) itera todas las filas.'
  };
}

function generateGenericVariableSuggestion(parsed: ParsedDaxExpression): Suggestion | null {
  // Only suggest if there are measures used multiple times
  if (parsed.measures.length === 0) return null;

  return {
    id: 'add-variables',
    title: 'Considerar uso de variables',
    description: 'Tu código tiene múltiples funciones. Variables pueden mejorar la legibilidad y potencialmente la performance.',
    originalCode: 'Código actual sin variables',
    suggestedCode: `-- Patrón recomendado:
VAR Paso1 = CALCULATE(...)
VAR Paso2 = FILTER(...)
VAR Resultado = SUMX(Paso2, ...)
RETURN
    Resultado`,
    impact: 'low',
    reason: 'Variables hacen el código más mantenible y pueden prevenir recálculos innecesarios.'
  };
}

export function calculateScore(
  parsed: ParsedDaxExpression,
  issues: Issue[]
): number {
  let score = 100;

  // Deduct points for issues
  issues.forEach(issue => {
    switch (issue.severity) {
      case 'critical':
        score -= 25;
        break;
      case 'warning':
        score -= 10;
        break;
      case 'info':
        score -= 5;
        break;
    }
  });

  // Bonus for good practices
  if (parsed.variables.length > 0) {
    score += 5;
  }

  // Penalize high complexity
  if (parsed.functions.length > 10) {
    score -= 10;
  }

  return Math.max(0, Math.min(100, score));
}
