# ⚡ DAX Optimizer

Herramienta de análisis y optimización de código DAX para Power BI.

## Características

- 📝 **Editor de código DAX** - Interfaz intuitiva para escribir y pegar código DAX
- 🔍 **Análisis automático** - Detecta problemas de performance y anti-patrones
- 📊 **Score de performance** - Evaluación visual del código (0-100)
- 📈 **Métricas detalladas** - Complejidad, iteradores anidados, transiciones de contexto
- 🔴 **Problemas detectados** - Lista detallada de issues con severidad (crítico, warning, info)
- 💡 **Sugerencias de optimización** - Recomendaciones con ejemplos de código mejorado
- ✅ **Validación** - Confirma cuando el código está optimizado

## Problemas que detecta

### Performance (Crítico)
- ❌ Iteradores anidados (SUMX dentro de SUMX)
- ❌ ALL() usado en FILTER sobre tabla completa
- ❌ Medidas usadas en columnas calculadas

### Context Transition (Warning)
- ⚠️ CALCULATE anidado innecesario
- ⚠️ FILTER sin KEEPFILTERS

### Code Quality (Info)
- ℹ️ Código complejo sin variables
- ℹ️ Expresiones repetidas sin VAR
- ℹ️ Referencias a medidas repetidas

## Sugerencias que ofrece

- Eliminar iteradores anidados usando VAR
- Usar KEEPFILTERS para mantener contexto
- Introducir variables (VAR) para mejorar legibilidad y performance
- Aplanar CALCULATEs anidados
- Optimizar uso de ALL en FILTER
- Y más...

## Instalación

### Primera vez

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno:
```bash
venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Simplemente ejecuta:
```bash
run_dax_optimizer.bat
```

O manualmente:
```bash
cd streamlit_app
streamlit run app.py
```

## Estructura del Proyecto

```
dax-optimizer-streamlit/
├── core/                   # Módulo de análisis
│   ├── __init__.py
│   ├── dax_parser.py      # Parser de código DAX
│   ├── dax_analyzer.py    # Detector de problemas
│   └── dax_suggestions.py # Generador de sugerencias
├── streamlit_app/
│   └── app.py             # Aplicación Streamlit
├── requirements.txt
├── run_dax_optimizer.bat  # Script de inicio
└── README.md
```

## Tecnologías

- **Python 3.8+**
- **Streamlit** - Framework de aplicación web
- **Plotly** - Gráficos interactivos
- **Pandas** - Manipulación de datos

## Créditos

Desarrollado con ❤️ usando Streamlit
