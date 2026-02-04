# ⚡ DAX Optimizer v1.1

**Análisis avanzado de medidas DAX con sistema de tolerancia**

> Desarrollado por **Adrián Javier Messina** | Enero 2026

[![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📚 Documentación

- **[README.md](README.md)** - Este archivo, introducción y setup
- **[CHANGELOG.md](CHANGELOG.md)** - Historial completo de cambios
- **[ROADMAP.md](ROADMAP.md)** - Roadmap de desarrollo completo
- **[PROPUESTAS_MEJORAS.md](PROPUESTAS_MEJORAS.md)** - Ideas y propuestas de mejoras
- **[FASE2_DIFERENCIACION.md](FASE2_DIFERENCIACION.md)** - Especificación técnica detallada de Fase 2
- **[QUICK_START_FASE2.md](QUICK_START_FASE2.md)** - Guía rápida para implementar Fase 2

## Novedades v1.1

### Nuevas funcionalidades

1. **Analizar archivos PBIP completos**
   - Extracción automática de TODAS las medidas del modelo
   - Soporte para formatos model.bim (JSON) y TMDL (texto)
   - Validación de archivos PBIP

2. **Ranking de medidas problemáticas**
   - Tabla con todas las medidas ordenadas por impacto
   - Score de 0-100 para cada medida
   - Filtros por prioridad y búsqueda

3. **Score de impacto**
   - Algoritmo de priorización basado en:
     - Problemas críticos detectados
     - Complejidad del código
     - Iteradores anidados
     - Transiciones de contexto
   - Clasificación en 4 niveles: Crítico, Alto, Medio, Bajo

4. **Vista detallada por medida**
   - Expandir cualquier medida para ver análisis completo
   - Código DAX completo
   - Problemas detectados
   - Sugerencias de optimización
   - Métricas de performance

## Instalación

### Requisitos previos

- Python 3.8 o superior
- pip

### Pasos de instalación

1. Clonar o descargar este repositorio

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Iniciar la aplicación

```bash
streamlit run streamlit_app/app.py
```

O usar el archivo batch (Windows):
```bash
run_dax_optimizer.bat
```

### Analizar un archivo PBIP

1. Carga tu archivo PBIP (.pbip) usando el botón de upload
2. Espera a que se extraigan y analicen todas las medidas
3. Revisa las estadísticas generales y distribución de prioridades
4. Explora la tabla de medidas rankeadas
5. Expande cualquier medida para ver el análisis detallado

## Criterios de evaluación

### Score de impacto (0-100)

- **🔴 Crítico (0-40)**
  - Iteradores anidados
  - FILTER con ALL sobre tabla completa
  - Complejidad > 70
  - Medidas en columnas calculadas

- **🟠 Alto (41-60)**
  - Múltiples warnings
  - Complejidad 50-70
  - Múltiples transiciones de contexto

- **🟡 Medio (61-75)**
  - Algunos warnings
  - Complejidad 30-50
  - Código sin variables

- **🟢 Bajo (76-100)**
  - Bien optimizado
  - Complejidad < 30
  - Uso correcto de variables

## Arquitectura

### Estructura de archivos

```
dax-optimizer-streamlit-v1.1/
├── core/
│   ├── __init__.py
│   ├── dax_parser.py          # Parser de código DAX
│   ├── dax_analyzer.py         # Detección de problemas
│   ├── dax_suggestions.py      # Generación de sugerencias
│   ├── pbip_extractor.py       # Extracción de medidas PBIP [NUEVO]
│   └── measure_ranker.py       # Sistema de ranking [NUEVO]
├── streamlit_app/
│   ├── __init__.py
│   └── app.py                  # Aplicación Streamlit [RENOVADO]
├── requirements.txt
├── README.md
└── run_dax_optimizer.bat
```

### Módulos principales

#### pbip_extractor.py
- `extract_measures_from_pbip()`: Extrae todas las medidas de un PBIP
- `parse_model_bim()`: Parsea archivos model.bim (JSON)
- `parse_tmdl_files()`: Parsea archivos TMDL (texto)
- `validate_pbip_file()`: Valida estructura del archivo

#### measure_ranker.py
- `calculate_impact_score()`: Calcula score de impacto 0-100
- `rank_measures()`: Ordena medidas por impacto
- `get_priority_label()`: Asigna etiqueta de prioridad
- `get_summary_stats()`: Estadísticas generales
- `get_top_issues()`: Issues más frecuentes

#### app.py (renovado)
- Interfaz completamente rediseñada
- Upload de archivos PBIP
- Dashboard con estadísticas
- Tabla de ranking interactiva
- Vista detallada expandible por medida

## Formatos PBIP soportados

### model.bim (JSON)
Estructura típica de Power BI Desktop
```json
{
  "model": {
    "tables": [
      {
        "name": "Sales",
        "measures": [
          {
            "name": "Total Sales",
            "expression": "SUM(Sales[Amount])"
          }
        ]
      }
    ]
  }
}
```

### TMDL (Text Model Definition Language)
Formato de texto nuevo de Power BI
```
measure 'Total Sales' =
    SUM(Sales[Amount])
```

## Problemas detectados

### Críticos (🔴)
- Iteradores anidados (SUMX dentro de SUMX)
- FILTER(ALL(Tabla), ...) sobre tabla completa
- Medidas usadas en columnas calculadas
- Transiciones de contexto innecesarias

### Warnings (⚠️)
- FILTER sin KEEPFILTERS en CALCULATE
- CALCULATEs anidados
- Expresiones repetidas sin variables
- Funciones costosas (CROSSJOIN, GENERATE, LOOKUPVALUE)

### Info (ℹ️)
- Código complejo sin variables
- Referencias repetidas a medidas
- Oportunidades de refactorización

## Recursos

- [SQLBI - DAX Patterns](https://www.sqlbi.com/patterns/)
- [DAX Guide](https://dax.guide/)
- [Power BI Best Practices](https://docs.microsoft.com/power-bi/)
- [Optimizing DAX](https://www.sqlbi.com/articles/optimizing-dax-expressions/)

## Versiones

### v1.1 (Actual)
- Análisis completo de archivos PBIP
- Ranking de medidas por impacto
- Sistema de scoring mejorado
- Interfaz renovada con vista expandible

### v1.0
- Análisis de medidas individuales
- Detección de anti-patrones
- Sugerencias de optimización

## Licencia

MIT License

## Autor

DAX Optimizer Team
