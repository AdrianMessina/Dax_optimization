# 🚀 Suite de Optimización DAX

**Conjunto completo de herramientas para analizar y optimizar consultas DAX en Power BI**

> Desarrollado por **Adrián Javier Messina** | YPF S.A. | Enero 2026

[![Version](https://img.shields.io/badge/version-1.1-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-19-blue.svg)](https://react.dev)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📚 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Aplicaciones](#aplicaciones)
- [Inicio Rápido](#inicio-rápido)
- [Características](#características)
- [Instalación](#instalación)
- [Documentación](#documentación)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## 🎯 Descripción General

Este repositorio contiene un conjunto de herramientas diseñadas para ayudar a los desarrolladores de Power BI a optimizar su código DAX mediante la detección de anti-patrones, medición de complejidad y sugerencias prácticas de mejora.

### Aplicaciones Incluidas

Este repositorio contiene tres aplicaciones con diferentes enfoques:

1. **dax-optimizer** - Aplicación web React/TypeScript con Monaco Editor
2. **dax-optimizer-streamlit** - Aplicación web Python/Streamlit básica para análisis rápidos
3. **dax-optimizer-streamlit-v1.1** - Versión avanzada con soporte para archivos PBIP y ranking de medidas

## 🚀 Inicio Rápido

### Opción 1: Streamlit Avanzado (Recomendado)

```bash
cd dax-optimizer-streamlit-v1.1
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

### Opción 2: Aplicación Web React

```bash
cd dax-optimizer
npm install
npm run dev
```

### Opción 3: Streamlit Básico

```bash
cd dax-optimizer-streamlit
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

## ⭐ Características

### Capacidades Principales

- ✅ **Detección de Patrones DAX**: Identifica anti-patrones y problemas de rendimiento
- ✅ **Puntuación de Complejidad**: Mide la complejidad del código (escala 0-100)
- ✅ **Soporte de Archivos PBIP**: Analiza archivos completos de Power BI Project
- ✅ **Ranking de Medidas**: Prioriza medidas por impacto y potencial de optimización
- ✅ **Sugerencias Inteligentes**: Proporciona recomendaciones específicas de optimización
- ✅ **Múltiples Interfaces**: Elige entre React, Streamlit básico o Streamlit avanzado

### Capacidades de Detección

#### 🔴 Problemas Críticos
- Iteradores anidados (SUMX dentro de SUMX)
- FILTER(ALL(Tabla), ...) en tablas completas
- Medidas usadas en columnas calculadas
- Transiciones de contexto innecesarias

#### ⚠️ Advertencias
- FILTER sin KEEPFILTERS en CALCULATE
- Funciones CALCULATE anidadas
- Expresiones repetidas sin variables
- Funciones costosas (CROSSJOIN, GENERATE, LOOKUPVALUE)

#### ℹ️ Información
- Código complejo sin variables
- Referencias a medidas repetidas
- Oportunidades de refactorización

## 📦 Instalación

### Prerequisitos

- **Para aplicaciones Python**: Python 3.8+ y pip
- **Para aplicación React**: Node.js 18+ y npm

### Configuración de Proxy Corporativo

Si estás detrás de un proxy corporativo:

```bash
export HTTPS_PROXY=http://proxy-azure
export HTTP_PROXY=http://proxy-azure

# Instalar paquetes Python
pip install -r requirements.txt

# O instalar paquetes Node
npm install
```

## 📖 Documentación

Cada aplicación tiene su propia documentación detallada:

- **[dax-optimizer-streamlit-v1.1/README.md](dax-optimizer-streamlit-v1.1/README.md)** - Versión Streamlit avanzada (recomendada)
- **[dax-optimizer/README.md](dax-optimizer/README.md)** - Aplicación web React
- **[dax-optimizer-streamlit/README.md](dax-optimizer-streamlit/README.md)** - Versión Streamlit básica

Documentación adicional:

- **[CHANGELOG.md](dax-optimizer-streamlit-v1.1/CHANGELOG.md)** - Historial de versiones
- **[ROADMAP.md](dax-optimizer-streamlit-v1.1/ROADMAP.md)** - Planes de desarrollo futuros

## 🏗️ Arquitectura

```
dax-optimization/
├── dax-optimizer/                      # Aplicación React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   ├── package.json
│   └── README.md
│
├── dax-optimizer-streamlit/            # Aplicación Streamlit básica
│   ├── core/
│   │   ├── dax_parser.py
│   │   ├── dax_analyzer.py
│   │   └── dax_suggestions.py
│   ├── streamlit_app/
│   │   └── app.py
│   ├── requirements.txt
│   └── README.md
│
└── dax-optimizer-streamlit-v1.1/       # Aplicación Streamlit avanzada
    ├── core/
    │   ├── dax_parser.py
    │   ├── dax_analyzer.py
    │   ├── dax_suggestions.py
    │   ├── pbip_extractor.py          # NUEVO: Soporte PBIP
    │   └── measure_ranker.py           # NUEVO: Sistema de ranking
    ├── streamlit_app/
    │   └── app.py
    ├── requirements.txt
    └── README.md
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes sugerencias o mejoras:

1. Haz un fork del repositorio
2. Crea una rama de funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Confirma tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Empuja a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Construido con [Streamlit](https://streamlit.io/)
- Construido con [React](https://react.dev/) y [Vite](https://vitejs.dev/)
- Mejores prácticas DAX de [SQLBI](https://www.sqlbi.com/)
- Documentación de Power BI de [Microsoft](https://learn.microsoft.com/power-bi/)

## 📧 Contacto

**Adrián Javier Messina**
Desarrollador de visualización Sr. - YPF S.A.
Email: adrianjavier.messina@set.ypf.com

---

**Hecho con ❤️ para la comunidad de Power BI**
