# ⚡ DAX Optimizer

Analizador y optimizador de código DAX para Power BI. Detecta anti-patterns, problemas de performance y genera sugerencias automáticas de optimización.

## 🚀 Características

### Detección de Anti-Patterns
- **Iteradores Anidados**: Detecta SUMX, AVERAGEX, etc. anidados que causan complejidad O(n²)
- **CALCULATE Anidado**: Identifica transiciones de contexto innecesarias
- **FILTER sin KEEPFILTERS**: Detecta sobreescritura de contexto de filtro
- **ALL en FILTER**: Identifica iteraciones ineficientes sobre tablas completas
- **Funciones Costosas**: Alerta sobre CROSSJOIN, GENERATE, LOOKUPVALUE, etc.
- **Context Transitions**: Detecta medidas en columnas calculadas
- **Código sin Variables**: Identifica expresiones repetidas que deberían usar VAR

### Sugerencias Automáticas
- Refactorización con variables (VAR)
- Aplanamiento de CALCULATE anidados
- Uso de KEEPFILTERS
- Alternativas a funciones costosas
- Ejemplos de código optimizado con explicaciones

### Métricas de Performance
- Puntuación de performance (0-100)
- Complejidad del código
- Contador de iteradores anidados
- Transiciones de contexto
- Variables utilizadas

## 🛠️ Tecnologías

- **React** + **TypeScript**
- **Vite** (build tool)
- **Monaco Editor** (editor de código)
- Parser DAX personalizado
- Motor de análisis de patrones

## 📦 Instalación

```bash
npm install
```

## 🏃 Ejecución

```bash
npm run dev
```

La aplicación se abrirá en [http://localhost:5173](http://localhost:5173)

## 🧪 Uso

1. Pega tu código DAX (medida, columna calculada o tabla calculada) en el editor
2. Haz clic en **"Analizar Código"**
3. Revisa:
   - **Puntuación de Performance**: Score general de 0-100
   - **Métricas**: Complejidad, iteradores anidados, context transitions
   - **Problemas Detectados**: Issues con severidad (crítico, warning, info)
   - **Sugerencias**: Código optimizado con explicaciones

## 📚 Ejemplos de Detección

### ❌ Iteradores Anidados
```dax
Total Sales =
SUMX(
    Customers,
    SUMX(
        FILTER(Sales, Sales[CustomerID] = Customers[ID]),
        Sales[Amount]
    )
)
```

### ✅ Optimizado
```dax
Total Sales =
SUMX(
    Customers,
    CALCULATE(SUM(Sales[Amount]))
)
```

---

### ❌ Sin Variables
```dax
Profit Margin =
IF(
    SUM(Sales[Revenue]) > 0,
    DIVIDE(
        SUM(Sales[Revenue]) - SUM(Sales[Cost]),
        SUM(Sales[Revenue])
    ),
    BLANK()
)
```

### ✅ Con Variables
```dax
Profit Margin =
VAR Revenue = SUM(Sales[Revenue])
VAR Cost = SUM(Sales[Cost])
VAR Profit = Revenue - Cost
RETURN
    DIVIDE(Profit, Revenue)
```

## 🔮 Roadmap Futuro (Nivel 2+)

- [ ] Integración con archivos .pbix/.pbip para análisis más profundo
- [ ] Detección de problemas de relaciones y cardinalidad
- [ ] Sugerencias basadas en tamaño de tablas
- [ ] Exportar reportes de análisis
- [ ] Integración con DAX Studio
- [ ] Análisis batch de múltiples medidas
- [ ] Comparación antes/después con métricas reales

## 📖 Recursos de Aprendizaje

- [SQLBI - DAX Optimization](https://www.sqlbi.com/articles/)
- [The Definitive Guide to DAX](https://www.sqlbi.com/books/the-definitive-guide-to-dax-2nd-edition/)
- [DAX Patterns](https://www.daxpatterns.com/)

## 🤝 Contribución

Este es un proyecto Nivel 1 (análisis sin modelo de datos). Sugerencias y mejoras son bienvenidas.

## 📄 Licencia

MIT
