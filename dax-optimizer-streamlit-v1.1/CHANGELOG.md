# Changelog

## [1.1.1] - 2026-02-02

### 🎯 Nuevas Funcionalidades

#### Sistema de Tolerancia
- **Control de umbral**: Slider interactivo para configurar tolerancia de riesgo (0-100)
- **Gauge visual**: Medidor circular que compara score promedio del reporte vs tolerancia configurada
- **Métricas dinámicas**:
  - Delta automático entre score actual y tolerancia
  - Contador de medidas fuera de tolerancia
  - Porcentaje de medidas que requieren atención
- **Indicadores visuales**: Colores adaptativos según cumplimiento de tolerancia

#### Visualización de Influencia
- **Gráfico de barras mejorado**: Top 10 medidas con mayor riesgo
- **Líneas de referencia**:
  - Línea roja (dash): Umbral de tolerancia configurado
  - Línea azul (dot): Score promedio del reporte
- **Contribución individual**: Cada medida muestra su aporte al score total en hover
- **Colores dinámicos**: Barra coloreada según nivel de riesgo de cada medida

#### Información del Desarrollador
- **Créditos agregados**: Adrián Javier Messina, Enero 2026
- **Sidebar actualizado**: Información del desarrollador y versión
- **Header mejorado**: Subtítulo con mención del autor

### Correcciones críticas

#### Bug fixes
- **Fix: Error "unbalanced parenthesis"**: Corregido error al analizar medidas con caracteres especiales en nombres (%, paréntesis, etc.)
  - Problema: Nombres de medidas con caracteres regex especiales causaban crash en `check_repeated_expressions()`
  - Solución: Uso de `re.escape()` para escapar caracteres especiales
  - Impacto: 431/431 medidas ahora se analizan correctamente (antes: 426/431)

- **Fix: Manejo de ruta PBIP**: Corregida lectura de archivos .pbip
  - Problema: La app no manejaba correctamente la ruta al archivo `.pbip`
  - Solución: Detección automática de carpeta `.SemanticModel` asociada
  - Acepta ahora: ruta al `.pbip`, ruta a `.SemanticModel`, o carpeta padre
  - Auto-remoción de comillas al copiar ruta con "Copiar como ruta de acceso"

#### Mejoras de robustez
- **Manejo de errores mejorado**: Si una medida falla al analizar, continúa con las demás
- **Regex optimizados**: Evita backtracking excesivo en patrones complejos
- **Validaciones NULL-safe**: Manejo correcto de metrics=None en casos de error

### Mejoras de UI/UX

#### Sistema de scoring rediseñado (BREAKING CHANGE)
- **Score invertido e intuitivo**: Cambio de "menor=peor" a "mayor=peor"
  - Antes: 0-100 (menor score = peor medida) ❌ confuso
  - Ahora: 0-100 (mayor score = mayor riesgo) ✅ intuitivo
- **Nueva nomenclatura**: "Score de Impacto" → "Score de Riesgo"
- **Rangos actualizados**:
  - 🔴 Crítico: 76-100 (antes: 0-40)
  - 🟠 Alto: 51-75 (antes: 41-60)
  - 🟡 Medio: 26-50 (antes: 61-75)
  - 🟢 Bajo: 0-25 (antes: 76-100)

#### Visualización simplificada
- **Badges de prioridad claros**: Un solo badge grande con color y emoji
- **Métricas consolidadas**: Reducción de métricas confusas a info clave
  - Eliminado: múltiples íconos y números confusos
  - Agregado: Score de Riesgo prominente + Total Issues
- **Gráfico mejorado**: Reemplazo de dona por barra horizontal
  - Nuevo: "Top 10 Medidas con Mayor Riesgo"
  - Visualización clara del score de cada medida
  - Colores según nivel de riesgo

#### Mejoras de interfaz
- **Instrucciones claras**: Guía paso a paso para copiar ruta PBIP
- **Info contextual**: Explicación de estructura de archivos PBIP
- **Help text mejorado**: Tooltips explicando qué significa cada métrica
- **Mensajes de error descriptivos**: Mensajes claros cuando algo falla

### Cambios técnicos

#### Archivos modificados
- `core/pbip_extractor.py`: Manejo de rutas .pbip y carpetas .SemanticModel
- `core/dax_analyzer.py`: Fix regex con `re.escape()`, patrones optimizados
- `core/measure_ranker.py`: Sistema de scoring invertido
- `streamlit_app/app.py`: UI rediseñada, nuevo gráfico, manejo de errores

#### Funciones actualizadas
- `calculate_impact_score()`: Lógica invertida para score intuitivo
- `get_priority_label()`: Rangos actualizados
- `rank_measures()`: Ordenamiento invertido (mayor riesgo primero)
- `render_measure_row()`: Diseño simplificado y claro
- `render_top_risky_measures()`: Nuevo gráfico de barras horizontales (reemplaza dona)

---

## [1.1.0] - 2026-01-30

### Nuevas funcionalidades

#### Análisis de archivos PBIP completos
- **Extractor PBIP completo**: Nuevo módulo `pbip_extractor.py` que extrae TODAS las medidas DAX de archivos PBIP
- **Soporte multi-formato**: Compatible con model.bim (JSON) y TMDL (formato de texto)
- **Validación de archivos**: Verificación automática de estructura PBIP antes del análisis
- **Información del modelo**: Visualización de tablas, medidas y tamaño del archivo

#### Sistema de ranking
- **Score de impacto**: Algoritmo que calcula un score de 0-100 para cada medida
- **Priorización automática**: Clasificación en 4 niveles (Crítico, Alto, Medio, Bajo)
- **Ordenamiento inteligente**: Las medidas más problemáticas aparecen primero
- **Módulo measure_ranker.py**: Sistema completo de ranking y estadísticas

#### Nueva interfaz
- **Dashboard de resumen**: Estadísticas generales del análisis
- **Gráfico de distribución**: Visualización de medidas por nivel de prioridad
- **Issues más frecuentes**: Top 5 de problemas más comunes en el modelo
- **Tabla interactiva**: Ranking de todas las medidas con filtros y búsqueda
- **Vista expandible**: Cada medida se puede expandir para ver análisis completo
- **Tabs organizados**: Código, Análisis, Sugerencias y Métricas en tabs separados

#### Mejoras en análisis
- **Score mejorado**: Algoritmo más sofisticado que considera múltiples factores
- **Penalizaciones específicas**: Puntos extras deducidos por patrones críticos
- **Bonus por buenas prácticas**: Puntos adicionales por uso de variables
- **Estadísticas agregadas**: Resumen de todo el modelo analizado

### Características técnicas

#### Módulos nuevos
- `core/pbip_extractor.py`: Extracción de medidas desde PBIP
  - `extract_measures_from_pbip()`: Función principal de extracción
  - `parse_model_bim()`: Parser para formato JSON
  - `parse_tmdl_files()`: Parser para formato TMDL
  - `validate_pbip_file()`: Validador de estructura
  - `get_pbip_info()`: Información general del archivo

- `core/measure_ranker.py`: Sistema de ranking
  - `calculate_impact_score()`: Cálculo de score de impacto
  - `rank_measures()`: Ordenamiento de medidas
  - `get_priority_label()`: Asignación de etiquetas
  - `get_summary_stats()`: Estadísticas del análisis
  - `filter_measures_by_priority()`: Filtrado por prioridad
  - `get_top_issues()`: Issues más frecuentes
  - `RankedMeasure`: Dataclass para medidas rankeadas

#### Interfaz renovada
- `streamlit_app/app.py`: Aplicación completamente rediseñada
  - Upload de archivos PBIP
  - Dashboard con métricas clave
  - Gráficos interactivos con Plotly
  - Tabla de ranking con filtros
  - Vista detallada expandible
  - Sistema de tabs para organizar información
  - Diseño profesional con CSS personalizado

### Dependencias
- `pyyaml==6.0.1`: Agregado para soporte de archivos TMDL
- Actualización de versiones de streamlit, plotly y pandas

### Criterios de evaluación

#### 🔴 Crítico (0-40 puntos)
- Iteradores anidados detectados
- FILTER con ALL sobre tabla completa
- Complejidad superior a 70
- Medidas usadas en columnas calculadas
- Múltiples problemas críticos acumulados

#### 🟠 Alto (41-60 puntos)
- Múltiples advertencias (3 o más)
- Complejidad entre 50-70
- Funciones costosas sin optimizar
- Múltiples transiciones de contexto

#### 🟡 Medio (61-75 puntos)
- Algunas advertencias (1-2)
- Complejidad entre 30-50
- Código sin variables pero funcional
- Oportunidades de mejora menores

#### 🟢 Bajo (76-100 puntos)
- Código bien optimizado
- Complejidad menor a 30
- Uso correcto de variables
- Sin problemas críticos ni advertencias

### Archivos de configuración
- `.streamlit/config.toml`: Configuración de tema y servidor
- `.gitignore`: Archivos a ignorar en control de versiones
- `CHANGELOG.md`: Este archivo

### Documentación
- README.md actualizado con:
  - Nuevas funcionalidades
  - Instrucciones de uso
  - Descripción de módulos
  - Criterios de evaluación
  - Ejemplos de formatos PBIP

---

## [1.0.0] - 2026-01-29

### Funcionalidades iniciales

- Análisis de medidas DAX individuales
- Detección de anti-patrones
- Parser de código DAX
- Sistema de issues (críticos, warnings, info)
- Generación de sugerencias de optimización
- Cálculo de métricas de performance
- Interfaz básica con Streamlit

### Módulos base
- `core/dax_parser.py`: Parser de código DAX
- `core/dax_analyzer.py`: Detección de problemas
- `core/dax_suggestions.py`: Generación de sugerencias
- `streamlit_app/app.py`: Interfaz simple

### Problemas detectados
- Iteradores anidados
- FILTER sin KEEPFILTERS
- Expresiones repetidas sin variables
- CALCULATEs anidados
- ALL en FILTER
- Funciones costosas
- Transiciones de contexto problemáticas
