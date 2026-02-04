# 🚀 Fase 2: Diferenciación - Especificación Técnica

**DAX Optimizer v2.0**
**Desarrollado por:** Adrián Javier Messina
**Fecha de Planificación:** Febrero 2026
**Estimación:** 3-4 semanas de desarrollo

---

## 📋 Índice

1. [Visión General](#visión-general)
2. [Feature 1: Auto-Optimización](#feature-1-auto-optimización)
3. [Feature 2: Grafo de Dependencias](#feature-2-grafo-de-dependencias)
4. [Feature 3: Análisis de Cardinalidad](#feature-3-análisis-de-cardinalidad)
5. [Arquitectura Técnica](#arquitectura-técnica)
6. [Plan de Implementación](#plan-de-implementación)
7. [Testing Strategy](#testing-strategy)
8. [Casos de Uso](#casos-de-uso)

---

## Visión General

### Objetivo
Convertir DAX Optimizer de una herramienta de **análisis** a una herramienta de **optimización activa**, permitiendo al usuario aplicar mejoras con un solo click y visualizar el impacto completo de las medidas en el modelo.

### Diferenciadores Clave
1. **Auto-Optimización**: Primera herramienta que permite aplicar optimizaciones automáticamente
2. **Grafo de Dependencias**: Visualización única de relaciones entre medidas
3. **Análisis de Cardinalidad**: Profundidad técnica que ninguna otra herramienta ofrece

### Stack Tecnológico
```
Frontend: Streamlit 1.30+
Visualización: Plotly 5.18+, NetworkX 3.2+
Análisis: Python 3.11+, Pandas 2.1+, Re
Persistencia: SQLite 3.40+ (para historial)
Testing: Pytest 7.4+
```

---

## Feature 1: Auto-Optimización

### 1.1 Descripción
Sistema que permite aplicar sugerencias de optimización automáticamente al código DAX, con preview, validación y rollback.

### 1.2 Funcionalidades

#### A. Refactoring Asistido
**Input:** Medida con issues detectados
**Output:** Código DAX optimizado

**Operaciones soportadas:**
1. **Introducir Variables (VAR)**
   - Detectar expresiones repetidas
   - Generar declaraciones VAR automáticamente
   - Reemplazar ocurrencias en código

2. **Aplanar CALCULATEs Anidados**
   - Detectar `CALCULATE(CALCULATE(...))`
   - Combinar filtros en un solo CALCULATE
   - Mantener semántica original

3. **Agregar KEEPFILTERS**
   - Detectar `CALCULATE(..., FILTER(...))`
   - Envolver FILTER con KEEPFILTERS
   - Preservar contexto

4. **Optimizar ALL en FILTER**
   - Detectar `FILTER(ALL(Table), ...)`
   - Reemplazar con CALCULATE + REMOVEFILTERS
   - Mejorar performance

#### B. Preview de Cambios
**Componente:** Split view lado a lado

```
┌─────────────────────────────────────────────────────┐
│ ❌ Código Original      │ ✅ Código Optimizado       │
├─────────────────────────┼────────────────────────────┤
│ CALCULATE(              │ VAR Result =               │
│   [Ventas],             │     CALCULATE(             │
│   FILTER(               │         [Ventas],          │
│     ALL(Clientes),      │         Clientes[País] =   │
│     Clientes[País] =    │             "Argentina",   │
│         "Argentina"     │         REMOVEFILTERS(     │
│   )                     │             Clientes       │
│ )                       │         )                  │
│                         │     )                      │
│                         │ RETURN Result              │
└─────────────────────────┴────────────────────────────┘
         [Aplicar] [Cancelar] [Copiar]
```

#### C. Validación Sintáctica
**Objetivo:** Asegurar que el código generado es válido

**Validaciones:**
1. **Paréntesis balanceados**: Verificar apertura/cierre
2. **Palabras clave DAX**: Validar sintaxis de funciones
3. **Referencias**: Verificar que tablas/columnas existan
4. **Variables**: Verificar uso correcto de VAR/RETURN

**Algoritmo:**
```python
def validate_dax_syntax(code: str) -> Tuple[bool, List[str]]:
    """
    Valida sintaxis básica de código DAX

    Returns:
        (es_valido, lista_de_errores)
    """
    errors = []

    # 1. Validar paréntesis
    if not are_parentheses_balanced(code):
        errors.append("Paréntesis desbalanceados")

    # 2. Validar VAR/RETURN
    if 'VAR' in code.upper() and 'RETURN' not in code.upper():
        errors.append("VAR sin RETURN correspondiente")

    # 3. Validar funciones DAX
    invalid_funcs = find_invalid_functions(code)
    if invalid_funcs:
        errors.append(f"Funciones inválidas: {invalid_funcs}")

    return len(errors) == 0, errors
```

### 1.3 Arquitectura

#### Módulo: `core/dax_optimizer.py`

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import re

@dataclass
class OptimizationAction:
    """Representa una acción de optimización"""
    id: str
    type: str  # 'add_variables', 'flatten_calculate', etc.
    description: str
    original_code: str
    optimized_code: str
    estimated_improvement: str  # 'high', 'medium', 'low'
    validation_result: Tuple[bool, List[str]]


class DaxOptimizer:
    """Motor de optimización de código DAX"""

    def __init__(self):
        self.optimizations = []

    def suggest_optimizations(self, parsed_dax, issues) -> List[OptimizationAction]:
        """
        Genera lista de optimizaciones aplicables

        Args:
            parsed_dax: Expresión DAX parseada
            issues: Lista de issues detectados

        Returns:
            Lista de acciones de optimización
        """
        actions = []

        for issue in issues:
            if issue.id == 'missing-variables':
                action = self._generate_add_variables(parsed_dax)
                actions.append(action)

            elif issue.id == 'nested-calculate':
                action = self._generate_flatten_calculate(parsed_dax)
                actions.append(action)

            elif issue.id == 'filter-without-keepfilters':
                action = self._generate_add_keepfilters(parsed_dax)
                actions.append(action)

            elif issue.id == 'all-in-filter':
                action = self._generate_optimize_all_filter(parsed_dax)
                actions.append(action)

        return actions

    def _generate_add_variables(self, parsed_dax) -> OptimizationAction:
        """Genera código con variables para expresiones repetidas"""
        original = parsed_dax.raw

        # Detectar expresiones repetidas
        repeated_exprs = self._find_repeated_expressions(original)

        if not repeated_exprs:
            return None

        # Generar código optimizado
        optimized = self._refactor_with_variables(original, repeated_exprs)

        # Validar
        is_valid, errors = validate_dax_syntax(optimized)

        return OptimizationAction(
            id='add_vars_001',
            type='add_variables',
            description='Introducir variables para expresiones repetidas',
            original_code=original,
            optimized_code=optimized,
            estimated_improvement='medium',
            validation_result=(is_valid, errors)
        )

    def _find_repeated_expressions(self, code: str) -> Dict[str, int]:
        """
        Encuentra expresiones que se repiten en el código

        Returns:
            Dict con expresión -> número de ocurrencias
        """
        # Patrón para capturar expresiones de CALCULATE
        calculate_pattern = r'CALCULATE\s*\([^)]+\)'
        matches = re.findall(calculate_pattern, code, re.IGNORECASE)

        counts = {}
        for match in matches:
            normalized = ' '.join(match.split())
            counts[normalized] = counts.get(normalized, 0) + 1

        # Retornar solo las que se repiten (>1)
        return {expr: count for expr, count in counts.items() if count > 1}

    def _refactor_with_variables(self, code: str, repeated: Dict[str, int]) -> str:
        """
        Refactoriza código introduciendo variables

        Args:
            code: Código original
            repeated: Dict de expresiones repetidas

        Returns:
            Código refactorizado con VAR/RETURN
        """
        optimized = code
        var_declarations = []
        var_counter = 1

        # Para cada expresión repetida
        for expr, count in repeated.items():
            var_name = f"_Var{var_counter}"
            var_counter += 1

            # Crear declaración VAR
            var_declarations.append(f"VAR {var_name} = {expr}")

            # Reemplazar ocurrencias
            optimized = optimized.replace(expr, var_name)

        # Construir código final
        if var_declarations:
            vars_block = '\n'.join(var_declarations)
            optimized = f"{vars_block}\nRETURN\n    {optimized}"

        return optimized

    def _generate_flatten_calculate(self, parsed_dax) -> OptimizationAction:
        """Aplana CALCULATEs anidados"""
        # Implementación similar...
        pass

    def _generate_add_keepfilters(self, parsed_dax) -> OptimizationAction:
        """Agrega KEEPFILTERS a FILTERs en CALCULATE"""
        # Implementación similar...
        pass

    def _generate_optimize_all_filter(self, parsed_dax) -> OptimizationAction:
        """Optimiza FILTER(ALL(...))"""
        # Implementación similar...
        pass

    def apply_optimization(self, action: OptimizationAction) -> str:
        """
        Aplica una optimización y retorna el código resultante

        Args:
            action: Acción de optimización a aplicar

        Returns:
            Código optimizado
        """
        # Validar antes de aplicar
        is_valid, errors = action.validation_result

        if not is_valid:
            raise ValueError(f"No se puede aplicar optimización inválida: {errors}")

        return action.optimized_code


def validate_dax_syntax(code: str) -> Tuple[bool, List[str]]:
    """Valida sintaxis básica de código DAX"""
    errors = []

    # Validar paréntesis
    if not _are_parentheses_balanced(code):
        errors.append("Paréntesis desbalanceados")

    # Validar VAR/RETURN
    has_var = bool(re.search(r'\bVAR\b', code, re.IGNORECASE))
    has_return = bool(re.search(r'\bRETURN\b', code, re.IGNORECASE))

    if has_var and not has_return:
        errors.append("VAR sin RETURN correspondiente")

    return len(errors) == 0, errors


def _are_parentheses_balanced(code: str) -> bool:
    """Verifica que los paréntesis estén balanceados"""
    stack = []
    for char in code:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0
```

### 1.4 UI Component

```python
# En streamlit_app/app.py

def render_optimization_panel(measure, ranked_measures):
    """Renderiza panel de auto-optimización"""

    st.markdown("### ⚙️ Optimización Automática")

    # Generar sugerencias de optimización
    optimizer = DaxOptimizer()
    parsed = parse_dax_code(measure.expression)
    optimizations = optimizer.suggest_optimizations(parsed, measure.issues)

    if not optimizations:
        st.info("✅ No se encontraron optimizaciones automáticas aplicables")
        return

    st.success(f"🎯 {len(optimizations)} optimización(es) disponible(s)")

    # Mostrar cada optimización
    for idx, action in enumerate(optimizations):
        with st.expander(f"🔧 {action.description}", expanded=idx==0):

            # Información
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Mejora estimada", action.estimated_improvement.upper())
            with col2:
                is_valid, errors = action.validation_result
                if is_valid:
                    st.success("✅ Validación: OK")
                else:
                    st.error(f"❌ Errores: {', '.join(errors)}")

            # Preview lado a lado
            col_orig, col_opt = st.columns(2)

            with col_orig:
                st.markdown("**❌ Original:**")
                st.code(action.original_code, language='dax')

            with col_opt:
                st.markdown("**✅ Optimizado:**")
                st.code(action.optimized_code, language='dax')

            # Botones de acción
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

            with col_btn1:
                if st.button("Copiar código", key=f"copy_{idx}"):
                    st.code(action.optimized_code)
                    st.success("Código copiado!")

            with col_btn2:
                if st.button("Aplicar", key=f"apply_{idx}",
                            disabled=not is_valid):
                    # Aplicar optimización
                    try:
                        optimized_code = optimizer.apply_optimization(action)
                        st.session_state[f'optimized_{measure.name}'] = optimized_code
                        st.success("✅ Optimización aplicada!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

            # Comparación de scores
            if is_valid:
                st.markdown("---")
                st.markdown("**📊 Impacto estimado:**")

                # Re-analizar código optimizado
                parsed_opt = parse_dax_code(action.optimized_code)
                issues_opt, metrics_opt = analyze_dax(parsed_opt)
                score_opt = calculate_score(parsed_opt, issues_opt)

                # Calcular mejora
                original_risk = 100 - measure.impact_score
                optimized_risk = 100 - score_opt
                improvement = original_risk - optimized_risk

                col_before, col_after, col_delta = st.columns(3)

                with col_before:
                    st.metric("Score Antes", f"{measure.impact_score}/100")

                with col_after:
                    st.metric("Score Después", f"{score_opt}/100")

                with col_delta:
                    st.metric("Mejora", f"{improvement:+.0f} puntos",
                             delta=f"{(improvement/measure.impact_score*100):.1f}%",
                             delta_color="normal")
```

---

## Feature 2: Grafo de Dependencias

### 2.1 Descripción
Visualización interactiva de las relaciones entre medidas, mostrando qué medidas usan a otras, detectando dependencias circulares y medidas huérfanas.

### 2.2 Funcionalidades

#### A. Extracción de Dependencias
**Input:** Todas las medidas del modelo
**Output:** Grafo dirigido de dependencias

**Tipos de relaciones:**
1. **Medida → Medida**: Una medida usa otra
2. **Medida → Tabla**: Una medida usa una tabla
3. **Medida → Columna**: Una medida usa una columna

#### B. Visualización de Grafo
**Componente:** NetworkX + Plotly

```
       [Total Ventas]
            ↓
     ┌──────┴──────┐
     ↓             ↓
[Ventas Netas] [Ventas Brutas]
     ↓             ↓
     └──────┬──────┘
            ↓
      [% Margen]
```

**Características:**
- **Nodos coloreados** según nivel de riesgo
- **Flechas dirigidas** mostrando dependencias
- **Hover info** con detalles de la medida
- **Click** para filtrar/expandir
- **Zoom/Pan** interactivo

#### C. Análisis de Dependencias

**Métricas calculadas:**
1. **Dependencias entrantes**: Cuántas medidas dependen de esta
2. **Dependencias salientes**: Cuántas medidas usa esta
3. **Profundidad**: Niveles de anidamiento
4. **Criticidad**: Si optimizar esta medida mejora otras

**Detecciones especiales:**
- ⚠️ **Dependencias circulares**: A → B → A (error de diseño)
- 🗑️ **Medidas huérfanas**: No usadas por ninguna otra
- 🔥 **Cuellos de botella**: Muchas medidas dependen de esta
- 🌳 **Medidas raíz**: No dependen de ninguna otra

### 2.3 Arquitectura

#### Módulo: `core/dependency_analyzer.py`

```python
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
import networkx as nx
import re

@dataclass
class Dependency:
    """Representa una dependencia entre medidas"""
    source: str  # Medida que usa
    target: str  # Medida usada
    type: str    # 'measure', 'table', 'column'


@dataclass
class MeasureNode:
    """Nodo del grafo de dependencias"""
    name: str
    risk_score: int
    dependencies_in: int  # Cuántas dependen de esta
    dependencies_out: int  # Cuántas usa esta
    depth: int  # Profundidad en el árbol
    is_orphan: bool
    is_root: bool
    is_bottleneck: bool


class DependencyAnalyzer:
    """Analizador de dependencias entre medidas"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.measures_map = {}

    def build_dependency_graph(self, ranked_measures: List) -> nx.DiGraph:
        """
        Construye grafo de dependencias

        Args:
            ranked_measures: Lista de medidas rankeadas

        Returns:
            Grafo dirigido de dependencias
        """
        # Crear mapa de medidas
        for measure in ranked_measures:
            self.measures_map[measure.name] = measure
            self.graph.add_node(
                measure.name,
                risk_score=measure.impact_score,
                expression=measure.expression
            )

        # Extraer dependencias
        for measure in ranked_measures:
            deps = self._extract_dependencies(measure)

            for dep in deps:
                if dep.target in self.measures_map:
                    # Agregar arista
                    self.graph.add_edge(dep.source, dep.target, type=dep.type)

        return self.graph

    def _extract_dependencies(self, measure) -> List[Dependency]:
        """
        Extrae dependencias de una medida

        Args:
            measure: Medida a analizar

        Returns:
            Lista de dependencias encontradas
        """
        dependencies = []
        code = measure.expression

        # Patrón para detectar referencias a medidas: [NombreMedida]
        measure_pattern = r'\[([^\]]+)\]'
        matches = re.findall(measure_pattern, code)

        for match in matches:
            # Verificar si es una medida (no columna)
            if match in self.measures_map:
                dependencies.append(Dependency(
                    source=measure.name,
                    target=match,
                    type='measure'
                ))

        return dependencies

    def analyze_dependencies(self) -> Dict[str, MeasureNode]:
        """
        Analiza el grafo y retorna métricas de cada nodo

        Returns:
            Dict con nombre de medida -> MeasureNode
        """
        analysis = {}

        for node in self.graph.nodes():
            measure = self.measures_map[node]

            # Calcular métricas
            deps_in = self.graph.in_degree(node)  # Cuántas dependen de esta
            deps_out = self.graph.out_degree(node)  # Cuántas usa esta

            # Detectar características especiales
            is_orphan = deps_in == 0 and deps_out == 0
            is_root = deps_out == 0  # No usa ninguna otra
            is_bottleneck = deps_in >= 5  # Umbral configurable

            # Calcular profundidad (distancia desde raíces)
            depth = self._calculate_depth(node)

            analysis[node] = MeasureNode(
                name=node,
                risk_score=measure.impact_score,
                dependencies_in=deps_in,
                dependencies_out=deps_out,
                depth=depth,
                is_orphan=is_orphan,
                is_root=is_root,
                is_bottleneck=is_bottleneck
            )

        return analysis

    def _calculate_depth(self, node: str) -> int:
        """Calcula profundidad del nodo en el árbol"""
        try:
            # Encontrar nodos raíz (sin dependencias salientes)
            roots = [n for n in self.graph.nodes()
                    if self.graph.out_degree(n) == 0]

            if not roots:
                return 0

            # Calcular distancia mínima a cualquier raíz
            depths = []
            for root in roots:
                try:
                    path_length = nx.shortest_path_length(
                        self.graph, source=node, target=root
                    )
                    depths.append(path_length)
                except nx.NetworkXNoPath:
                    continue

            return min(depths) if depths else 0
        except:
            return 0

    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        Detecta dependencias circulares

        Returns:
            Lista de ciclos encontrados
        """
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []

    def get_impact_cascade(self, measure_name: str) -> Dict[str, int]:
        """
        Calcula el impacto en cascada de optimizar una medida

        Args:
            measure_name: Nombre de la medida a analizar

        Returns:
            Dict con medidas afectadas -> nivel de impacto
        """
        cascade = {}

        # Obtener todas las medidas que dependen de esta (directa/indirectamente)
        if measure_name not in self.graph:
            return cascade

        # BFS para encontrar descendientes
        descendants = nx.descendants(self.graph, measure_name)

        for desc in descendants:
            # Calcular distancia (nivel de impacto)
            try:
                distance = nx.shortest_path_length(
                    self.graph, source=measure_name, target=desc
                )
                cascade[desc] = distance
            except:
                pass

        return cascade

    def get_optimization_priority(self) -> List[Tuple[str, float]]:
        """
        Calcula prioridad de optimización considerando dependencias

        Returns:
            Lista de (medida, score_prioridad) ordenada
        """
        priorities = []

        for node in self.graph.nodes():
            measure = self.measures_map[node]

            # Score base de riesgo
            base_score = measure.impact_score

            # Bonus por dependencias entrantes (impacto en cascada)
            deps_in = self.graph.in_degree(node)
            cascade_bonus = deps_in * 5

            # Penalización por ser hoja (menos impacto)
            deps_out = self.graph.out_degree(node)
            leaf_penalty = 10 if deps_out == 0 else 0

            # Score final
            priority_score = base_score + cascade_bonus - leaf_penalty

            priorities.append((node, priority_score))

        # Ordenar por prioridad descendente
        priorities.sort(key=lambda x: x[1], reverse=True)

        return priorities
```

### 2.4 UI Component

```python
# En streamlit_app/app.py

def render_dependency_graph(ranked_measures):
    """Renderiza grafo de dependencias interactivo"""

    st.markdown("### 🕸️ Grafo de Dependencias")

    # Construir grafo
    analyzer = DependencyAnalyzer()
    graph = analyzer.build_dependency_graph(ranked_measures)

    # Análisis
    analysis = analyzer.analyze_dependencies()
    cycles = analyzer.detect_circular_dependencies()

    # Estadísticas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        orphans = sum(1 for n in analysis.values() if n.is_orphan)
        st.metric("Medidas huérfanas", orphans,
                 help="Medidas no usadas por ninguna otra")

    with col2:
        bottlenecks = sum(1 for n in analysis.values() if n.is_bottleneck)
        st.metric("Cuellos de botella", bottlenecks,
                 help="Medidas con >5 dependencias")

    with col3:
        st.metric("Dependencias totales", graph.number_of_edges())

    with col4:
        st.metric("Ciclos detectados", len(cycles),
                 delta="Error" if cycles else None,
                 delta_color="inverse")

    # Alertas
    if cycles:
        with st.expander("⚠️ Dependencias Circulares Detectadas", expanded=True):
            for cycle in cycles:
                cycle_str = " → ".join(cycle) + f" → {cycle[0]}"
                st.error(f"🔄 {cycle_str}")
            st.warning("Las dependencias circulares deben eliminarse del modelo.")

    # Filtros
    st.markdown("#### Filtrar visualización")
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        show_orphans = st.checkbox("Mostrar huérfanas", value=True)

    with col_f2:
        show_only_risky = st.checkbox("Solo medidas de riesgo", value=False)

    with col_f3:
        max_depth = st.slider("Profundidad máxima", 1, 10, 5)

    # Construir layout del grafo
    pos = nx.spring_layout(graph, k=2, iterations=50)

    # Preparar nodos
    node_trace = []
    for node in graph.nodes():
        node_analysis = analysis[node]

        # Filtros
        if not show_orphans and node_analysis.is_orphan:
            continue

        if show_only_risky and node_analysis.risk_score < 50:
            continue

        if node_analysis.depth > max_depth:
            continue

        x, y = pos[node]

        # Color según riesgo
        color = get_priority_color(node_analysis.risk_score)

        # Tamaño según dependencias entrantes
        size = 10 + (node_analysis.dependencies_in * 3)

        node_trace.append(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            text=[node[:20]],
            textposition='top center',
            marker=dict(
                size=size,
                color=color,
                line=dict(width=2, color='white')
            ),
            hovertemplate=(
                f"<b>{node}</b><br>"
                f"Riesgo: {node_analysis.risk_score}/100<br>"
                f"Usan esta medida: {node_analysis.dependencies_in}<br>"
                f"Usa otras medidas: {node_analysis.dependencies_out}<br>"
                f"Profundidad: {node_analysis.depth}<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))

    # Preparar aristas
    edge_trace = []
    for edge in graph.edges():
        source, target = edge

        if source not in pos or target not in pos:
            continue

        x0, y0 = pos[source]
        x1, y1 = pos[target]

        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=1, color='rgba(125,125,125,0.3)'),
            hoverinfo='none',
            showlegend=False
        ))

    # Crear figura
    fig = go.Figure(data=edge_trace + node_trace)

    fig.update_layout(
        title="Grafo de Dependencias de Medidas",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tabla de análisis
    st.markdown("#### 📊 Análisis de Impacto")

    # Priorización considerando dependencias
    priorities = analyzer.get_optimization_priority()

    # Mostrar top 10
    st.markdown("**Top 10 medidas a optimizar (considerando impacto en cascada):**")

    for idx, (measure_name, priority_score) in enumerate(priorities[:10], 1):
        node_analysis = analysis[measure_name]
        cascade = analyzer.get_impact_cascade(measure_name)

        with st.expander(f"{idx}. {measure_name} - Prioridad: {priority_score:.0f}"):
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Score de Riesgo", f"{node_analysis.risk_score}/100")

            with col_b:
                st.metric("Medidas afectadas", len(cascade),
                         help="Si optimizas esta, mejoran automáticamente estas otras")

            with col_c:
                st.metric("Dependencias entrantes", node_analysis.dependencies_in)

            if cascade:
                st.markdown("**Medidas que mejorarían:**")
                cascade_sorted = sorted(cascade.items(), key=lambda x: x[1])
                for affected, distance in cascade_sorted[:5]:
                    st.write(f"- {affected} (nivel {distance})")
```

---

## Feature 3: Análisis de Cardinalidad

### 3.1 Descripción
Estimación de cardinalidad (número de filas) procesadas por cada medida, permitiendo identificar operaciones sobre grandes volúmenes de datos.

### 3.2 Funcionalidades

#### A. Estimación de Cardinalidad
**Input:** Expresión DAX + metadata del modelo
**Output:** Estimación de filas procesadas

**Niveles de análisis:**
1. **Tabla completa**: ALL(Tabla) → cardinalidad total
2. **Tabla filtrada**: FILTER(Tabla, ...) → estimación basada en selectividad
3. **Valores únicos**: VALUES(Columna) → cardinalidad de columna
4. **Producto cartesiano**: CROSSJOIN → multiplicación de cardinalidades

#### B. Alertas de Cardinalidad
**Umbrales:**
- 🟢 **Bajo** (<10K filas): OK
- 🟡 **Medio** (10K-100K): Revisar
- 🟠 **Alto** (100K-1M): Optimizar
- 🔴 **Crítico** (>1M): Problema severo

#### C. Sugerencias basadas en Cardinalidad
**Ejemplos:**
- "Esta medida procesa ~500K filas. Considera agregar filtros."
- "SUMX sobre 2M filas. Usa medida base si es posible."
- "CROSSJOIN genera 10M filas. Muy costoso."

### 3.3 Arquitectura

#### Módulo: `core/cardinality_analyzer.py`

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
import re

@dataclass
class CardinalityEstimate:
    """Estimación de cardinalidad de una operación"""
    operation: str  # 'FILTER', 'ALL', 'VALUES', etc.
    table: str
    estimated_rows: int
    confidence: str  # 'high', 'medium', 'low'
    level: str  # 'low', 'medium', 'high', 'critical'


@dataclass
class TableMetadata:
    """Metadata de una tabla del modelo"""
    name: str
    row_count: int  # Cardinalidad total
    columns: Dict[str, int]  # Columna -> distinct count


class CardinalityAnalyzer:
    """Analizador de cardinalidad de operaciones DAX"""

    def __init__(self, model_metadata: Dict[str, TableMetadata]):
        self.metadata = model_metadata

    def analyze_expression(self, dax_expression: str) -> List[CardinalityEstimate]:
        """
        Analiza cardinalidad de una expresión DAX

        Args:
            dax_expression: Código DAX a analizar

        Returns:
            Lista de estimaciones de cardinalidad
        """
        estimates = []

        # Detectar operaciones sobre tablas

        # 1. ALL(Tabla)
        all_pattern = r'ALL\s*\(\s*([\'"]?\w+[\'"]?)\s*\)'
        for match in re.finditer(all_pattern, dax_expression, re.IGNORECASE):
            table = match.group(1).strip('\'"')

            if table in self.metadata:
                estimates.append(CardinalityEstimate(
                    operation='ALL',
                    table=table,
                    estimated_rows=self.metadata[table].row_count,
                    confidence='high',
                    level=self._get_cardinality_level(
                        self.metadata[table].row_count
                    )
                ))

        # 2. FILTER(Tabla, ...)
        filter_pattern = r'FILTER\s*\(\s*([\'"]?\w+[\'"]?)\s*,'
        for match in re.finditer(filter_pattern, dax_expression, re.IGNORECASE):
            table = match.group(1).strip('\'"')

            if table in self.metadata:
                # Estimación conservadora: 10% de la tabla
                selectivity = 0.1
                estimated = int(self.metadata[table].row_count * selectivity)

                estimates.append(CardinalityEstimate(
                    operation='FILTER',
                    table=table,
                    estimated_rows=estimated,
                    confidence='medium',
                    level=self._get_cardinality_level(estimated)
                ))

        # 3. VALUES(Columna)
        values_pattern = r'VALUES\s*\(\s*([\'"]?\w+[\'"]?)\[(\w+)\]\s*\)'
        for match in re.finditer(values_pattern, dax_expression, re.IGNORECASE):
            table = match.group(1).strip('\'"')
            column = match.group(2)

            if table in self.metadata and column in self.metadata[table].columns:
                distinct_count = self.metadata[table].columns[column]

                estimates.append(CardinalityEstimate(
                    operation='VALUES',
                    table=f"{table}[{column}]",
                    estimated_rows=distinct_count,
                    confidence='high',
                    level=self._get_cardinality_level(distinct_count)
                ))

        # 4. CROSSJOIN
        crossjoin_pattern = r'CROSSJOIN\s*\('
        if re.search(crossjoin_pattern, dax_expression, re.IGNORECASE):
            # Buscar las tablas involucradas
            # Esto es simplificado, requiere parsing más sofisticado
            estimates.append(CardinalityEstimate(
                operation='CROSSJOIN',
                table='multiple',
                estimated_rows=1000000,  # Estimación conservadora
                confidence='low',
                level='critical'
            ))

        return estimates

    def _get_cardinality_level(self, row_count: int) -> str:
        """Determina el nivel de cardinalidad"""
        if row_count < 10000:
            return 'low'
        elif row_count < 100000:
            return 'medium'
        elif row_count < 1000000:
            return 'high'
        else:
            return 'critical'

    def generate_cardinality_warnings(
        self, estimates: List[CardinalityEstimate]
    ) -> List[str]:
        """
        Genera advertencias basadas en cardinalidad

        Args:
            estimates: Lista de estimaciones

        Returns:
            Lista de advertencias
        """
        warnings = []

        for est in estimates:
            if est.level == 'critical':
                warnings.append(
                    f"⚠️ {est.operation} sobre {est.table} procesa "
                    f"~{est.estimated_rows:,} filas. Muy costoso!"
                )
            elif est.level == 'high':
                warnings.append(
                    f"⚠️ {est.operation} sobre {est.table} procesa "
                    f"~{est.estimated_rows:,} filas. Considera optimizar."
                )

        return warnings


def extract_model_metadata_from_pbip(pbip_path: str) -> Dict[str, TableMetadata]:
    """
    Extrae metadata del modelo desde PBIP

    Args:
        pbip_path: Ruta al archivo PBIP

    Returns:
        Dict con metadata de tablas
    """
    # Esto requiere parsear el TMDL o model.bim
    # para obtener información de las tablas

    # Ejemplo simplificado:
    metadata = {
        'Ventas': TableMetadata(
            name='Ventas',
            row_count=1500000,
            columns={
                'Producto': 500,
                'Cliente': 10000,
                'Fecha': 1095
            }
        ),
        'Clientes': TableMetadata(
            name='Clientes',
            row_count=10000,
            columns={
                'ClienteID': 10000,
                'País': 25,
                'Ciudad': 500
            }
        )
    }

    return metadata
```

### 3.4 UI Component

```python
# En streamlit_app/app.py

def render_cardinality_analysis(measure, model_metadata):
    """Renderiza análisis de cardinalidad"""

    st.markdown("#### 📊 Análisis de Cardinalidad")

    # Analizar
    analyzer = CardinalityAnalyzer(model_metadata)
    estimates = analyzer.analyze_expression(measure.expression)
    warnings = analyzer.generate_cardinality_warnings(estimates)

    if not estimates:
        st.info("No se detectaron operaciones sobre tablas para analizar")
        return

    # Mostrar advertencias
    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("✅ Cardinalidad bajo control")

    # Tabla de estimaciones
    st.markdown("**Operaciones detectadas:**")

    data = []
    for est in estimates:
        data.append({
            'Operación': est.operation,
            'Tabla/Columna': est.table,
            'Filas estimadas': f"{est.estimated_rows:,}",
            'Nivel': est.level.upper(),
            'Confianza': est.confidence
        })

    df = pd.DataFrame(data)

    # Colorear por nivel
    def highlight_level(row):
        colors = {
            'LOW': 'background-color: #d4edda',
            'MEDIUM': 'background-color: #fff3cd',
            'HIGH': 'background-color: #f8d7da',
            'CRITICAL': 'background-color: #f5c6cb; font-weight: bold'
        }
        return [colors.get(row['Nivel'], '')] * len(row)

    st.dataframe(
        df.style.apply(highlight_level, axis=1),
        use_container_width=True,
        hide_index=True
    )

    # Gráfico de cardinalidad
    if len(estimates) > 1:
        fig = go.Figure(data=[go.Bar(
            x=[est.operation + f" ({est.table})" for est in estimates],
            y=[est.estimated_rows for est in estimates],
            marker_color=[
                {'low': '#2ed573', 'medium': '#ffd32a',
                 'high': '#ffa502', 'critical': '#ff4757'}[est.level]
                for est in estimates
            ]
        )])

        fig.update_layout(
            title="Filas Procesadas por Operación",
            xaxis_title="Operación",
            yaxis_title="Filas estimadas",
            height=300,
            yaxis_type="log"  # Escala logarítmica
        )

        st.plotly_chart(fig, use_container_width=True)
```

---

## Arquitectura Técnica

### Estructura de Archivos

```
dax-optimizer-streamlit-v1.1/
├── core/
│   ├── __init__.py
│   ├── dax_parser.py              # ✅ Existente
│   ├── dax_analyzer.py            # ✅ Existente
│   ├── dax_suggestions.py         # ✅ Existente
│   ├── measure_ranker.py          # ✅ Existente
│   ├── pbip_extractor.py          # ✅ Existente
│   ├── dax_optimizer.py           # 🆕 NUEVO - Auto-optimización
│   ├── dependency_analyzer.py     # 🆕 NUEVO - Grafo dependencias
│   └── cardinality_analyzer.py    # 🆕 NUEVO - Análisis cardinalidad
│
├── streamlit_app/
│   ├── __init__.py
│   ├── app.py                     # Modificar - Agregar nuevos componentes
│   └── components/                # 🆕 NUEVO - Componentes modulares
│       ├── __init__.py
│       ├── optimization_panel.py
│       ├── dependency_graph.py
│       └── cardinality_panel.py
│
├── data/                          # 🆕 NUEVO - Para persistencia
│   └── optimizations_history.db  # SQLite para historial
│
├── tests/                         # 🆕 NUEVO - Tests
│   ├── test_optimizer.py
│   ├── test_dependencies.py
│   └── test_cardinality.py
│
├── docs/                          # Documentación
│   ├── FASE2_DIFERENCIACION.md    # Este documento
│   └── API_REFERENCE.md
│
└── requirements.txt               # Actualizar dependencias
```

### Dependencias Adicionales

```txt
# requirements.txt - AGREGAR:

# Grafo de dependencias
networkx==3.2
python-louvain==0.16

# Visualización avanzada
plotly==5.18.0
kaleido==0.2.1  # Export de gráficos

# Testing
pytest==7.4.3
pytest-cov==4.1.0

# Base de datos
sqlalchemy==2.0.23

# Utilidades
pydantic==2.5.0  # Validación de datos
```

### Flujo de Datos

```
┌─────────────────┐
│  PBIP File      │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────────┐
│  pbip_extractor.py                      │
│  - Extrae medidas                       │
│  - Extrae metadata de tablas            │
└────────┬────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────┐
│  dax_parser.py + dax_analyzer.py        │
│  - Parsea cada medida                   │
│  - Detecta issues                       │
└────────┬────────────────────────────────┘
         │
         ├─────────────────────┬──────────────────────┬─────────────────────┐
         ↓                     ↓                      ↓                     ↓
┌────────────────────┐ ┌──────────────────┐ ┌────────────────────┐ ┌──────────────────┐
│ measure_ranker.py  │ │ dax_optimizer.py │ │ dependency_        │ │ cardinality_     │
│ - Calcula scores   │ │ - Genera código  │ │ analyzer.py        │ │ analyzer.py      │
│ - Prioriza         │ │   optimizado     │ │ - Construye grafo  │ │ - Estima filas   │
└────────┬───────────┘ └────────┬─────────┘ └────────┬───────────┘ └────────┬─────────┘
         │                       │                    │                       │
         └───────────────────────┴────────────────────┴───────────────────────┘
                                         │
                                         ↓
                              ┌──────────────────────┐
                              │  Streamlit UI        │
                              │  - Dashboard         │
                              │  - Visualizaciones   │
                              │  - Interacción       │
                              └──────────────────────┘
```

---

## Plan de Implementación

### Sprint 1: Auto-Optimización (1 semana)

**Días 1-2: Core**
- [ ] Crear `core/dax_optimizer.py`
- [ ] Implementar `DaxOptimizer` class
- [ ] Implementar `_generate_add_variables()`
- [ ] Implementar `_generate_flatten_calculate()`
- [ ] Implementar `validate_dax_syntax()`

**Días 3-4: UI**
- [ ] Crear `streamlit_app/components/optimization_panel.py`
- [ ] Implementar preview lado a lado
- [ ] Implementar botones de acción
- [ ] Integrar con app principal

**Día 5: Testing**
- [ ] Escribir tests unitarios
- [ ] Testing de integración
- [ ] Testing manual con casos reales
- [ ] Documentación

### Sprint 2: Grafo de Dependencias (1.5 semanas)

**Días 1-3: Core**
- [ ] Crear `core/dependency_analyzer.py`
- [ ] Implementar `DependencyAnalyzer` class
- [ ] Implementar extracción de dependencias
- [ ] Implementar detección de ciclos
- [ ] Implementar análisis de impacto

**Días 4-6: Visualización**
- [ ] Crear `streamlit_app/components/dependency_graph.py`
- [ ] Implementar layout del grafo (NetworkX)
- [ ] Implementar visualización Plotly
- [ ] Implementar filtros interactivos
- [ ] Implementar tabla de análisis

**Día 7: Testing**
- [ ] Tests unitarios
- [ ] Tests con grafos complejos
- [ ] Testing de performance
- [ ] Documentación

### Sprint 3: Análisis de Cardinalidad (0.5 semanas)

**Días 1-2: Core**
- [ ] Crear `core/cardinality_analyzer.py`
- [ ] Implementar `CardinalityAnalyzer` class
- [ ] Implementar detección de operaciones
- [ ] Implementar estimación de filas
- [ ] Implementar generación de warnings

**Día 3: UI**
- [ ] Crear `streamlit_app/components/cardinality_panel.py`
- [ ] Implementar tabla de estimaciones
- [ ] Implementar gráfico de cardinalidad
- [ ] Integrar con medidas

### Sprint 4: Integración y Pulido (1 semana)

**Días 1-2: Integración**
- [ ] Integrar todos los componentes
- [ ] Refactorizar código duplicado
- [ ] Optimizar performance

**Días 3-4: UI/UX**
- [ ] Mejorar diseño visual
- [ ] Agregar animaciones
- [ ] Mejorar responsive
- [ ] Testing de usabilidad

**Día 5: Documentación**
- [ ] Actualizar README
- [ ] Actualizar CHANGELOG
- [ ] Crear guías de usuario
- [ ] Crear API reference

---

## Testing Strategy

### Tests Unitarios

```python
# tests/test_optimizer.py

import pytest
from core.dax_optimizer import DaxOptimizer, validate_dax_syntax

class TestDaxOptimizer:

    def test_validate_balanced_parentheses(self):
        code = "CALCULATE([Ventas], FILTER(Productos, Productos[Categoria] = \"A\"))"
        is_valid, errors = validate_dax_syntax(code)
        assert is_valid == True
        assert len(errors) == 0

    def test_validate_unbalanced_parentheses(self):
        code = "CALCULATE([Ventas], FILTER(Productos, Productos[Categoria] = \"A\")"
        is_valid, errors = validate_dax_syntax(code)
        assert is_valid == False
        assert "Paréntesis desbalanceados" in errors

    def test_generate_add_variables(self):
        optimizer = DaxOptimizer()

        # Mock parsed DAX con expresiones repetidas
        parsed = MockParsedDax(
            raw="SUM([A]) + SUM([A]) + SUM([A])"
        )

        action = optimizer._generate_add_variables(parsed)

        assert action is not None
        assert "VAR" in action.optimized_code
        assert "RETURN" in action.optimized_code
        assert action.optimized_code.count("SUM([A])") == 1  # Solo una vez


# tests/test_dependencies.py

class TestDependencyAnalyzer:

    def test_build_simple_graph(self):
        measures = [
            MockMeasure("A", "[B] + [C]"),
            MockMeasure("B", "SUM(Table[Col])"),
            MockMeasure("C", "AVERAGE(Table[Col])")
        ]

        analyzer = DependencyAnalyzer()
        graph = analyzer.build_dependency_graph(measures)

        assert graph.number_of_nodes() == 3
        assert graph.number_of_edges() == 2
        assert graph.has_edge("A", "B")
        assert graph.has_edge("A", "C")

    def test_detect_circular_dependency(self):
        measures = [
            MockMeasure("A", "[B]"),
            MockMeasure("B", "[C]"),
            MockMeasure("C", "[A]")
        ]

        analyzer = DependencyAnalyzer()
        graph = analyzer.build_dependency_graph(measures)
        cycles = analyzer.detect_circular_dependencies()

        assert len(cycles) > 0
        assert set(cycles[0]) == {"A", "B", "C"}


# tests/test_cardinality.py

class TestCardinalityAnalyzer:

    def test_estimate_all_table(self):
        metadata = {
            "Ventas": TableMetadata("Ventas", 100000, {})
        }

        analyzer = CardinalityAnalyzer(metadata)
        estimates = analyzer.analyze_expression("SUM(ALL(Ventas))")

        assert len(estimates) == 1
        assert estimates[0].estimated_rows == 100000
        assert estimates[0].level == "high"

    def test_estimate_filter(self):
        metadata = {
            "Ventas": TableMetadata("Ventas", 100000, {})
        }

        analyzer = CardinalityAnalyzer(metadata)
        estimates = analyzer.analyze_expression(
            "SUMX(FILTER(Ventas, Ventas[Amount] > 100), [Amount])"
        )

        assert len(estimates) == 1
        assert estimates[0].estimated_rows == 10000  # 10% selectivity
```

### Tests de Integración

```python
# tests/test_integration.py

class TestFullWorkflow:

    def test_analyze_and_optimize_measure(self):
        # 1. Cargar PBIP
        measures = extract_measures_from_pbip(TEST_PBIP_PATH)

        # 2. Analizar
        analyzed = []
        for m in measures:
            parsed = parse_dax_code(m['expression'])
            issues, metrics = analyze_dax(parsed)
            suggestions = generate_suggestions(parsed, issues)

            analyzed.append({
                'name': m['name'],
                'expression': m['expression'],
                'issues': issues,
                'metrics': metrics,
                'suggestions': suggestions
            })

        # 3. Rankear
        ranked = rank_measures(analyzed)

        # 4. Optimizar primera medida problemática
        problematic = [m for m in ranked if m.impact_score > 70][0]

        optimizer = DaxOptimizer()
        parsed = parse_dax_code(problematic.expression)
        optimizations = optimizer.suggest_optimizations(
            parsed, problematic.issues
        )

        assert len(optimizations) > 0

        # 5. Aplicar optimización
        action = optimizations[0]
        optimized_code = optimizer.apply_optimization(action)

        # 6. Verificar mejora
        parsed_opt = parse_dax_code(optimized_code)
        issues_opt, metrics_opt = analyze_dax(parsed_opt)

        assert len(issues_opt) < len(problematic.issues)
```

---

## Casos de Uso

### Caso de Uso 1: Auto-Optimización

**Actor:** Analista de BI
**Objetivo:** Optimizar medida con expresiones repetidas

**Flujo:**
1. Usuario analiza PBIP
2. Sistema detecta medida con 3 issues
3. Usuario expande medida en tabla
4. Sistema muestra panel de optimización
5. Sistema sugiere: "Introducir variables (VAR)"
6. Usuario ve preview lado a lado
7. Usuario hace click en "Aplicar"
8. Sistema valida y aplica optimización
9. Usuario copia código optimizado
10. Usuario actualiza medida en Power BI

**Resultado:** Medida optimizada con variables, score mejora de 75 a 40.

### Caso de Uso 2: Grafo de Dependencias

**Actor:** Arquitecto de Datos
**Objetivo:** Entender impacto de optimizar una medida

**Flujo:**
1. Usuario analiza PBIP
2. Usuario navega a tab "Dependencias"
3. Sistema muestra grafo de todas las medidas
4. Usuario identifica medida "Total Ventas" (roja, grande)
5. Usuario hace hover: "20 medidas dependen de esta"
6. Usuario filtra: "Solo medidas de riesgo"
7. Grafo se actualiza mostrando solo críticas
8. Usuario ve que optimizar "Total Ventas" mejora 20 medidas
9. Usuario prioriza esa medida

**Resultado:** Decisión informada sobre qué optimizar primero.

### Caso de Uso 3: Análisis de Cardinalidad

**Actor:** Desarrollador Power BI
**Objetivo:** Diagnosticar medida lenta

**Flujo:**
1. Usuario tiene medida que tarda 30 segundos
2. Usuario analiza en DAX Optimizer
3. Sistema muestra tab "Cardinalidad"
4. Sistema alerta: "FILTER(ALL(Ventas)) procesa ~2M filas"
5. Sistema sugiere: "Usa CALCULATE + REMOVEFILTERS"
6. Usuario ve estimación: 2M → 200K filas
7. Usuario aplica optimización
8. Usuario testa en Power BI
9. Medida ahora tarda 3 segundos

**Resultado:** 90% reducción en tiempo de ejecución.

---

## Métricas de Éxito

### KPIs Técnicos
- **Cobertura de tests**: >80%
- **Performance**: Análisis completo <30 segundos
- **Precisión de optimización**: >95% código válido generado
- **Reducción de riesgo**: Promedio 20+ puntos por medida optimizada

### KPIs de Producto
- **Adopción**: 50+ reportes analizados en primer mes
- **Optimizaciones aplicadas**: 100+ medidas mejoradas
- **Satisfacción**: NPS >40
- **Tiempo ahorrado**: 2+ horas por reporte analizado

---

## Próximos Pasos

1. **Revisar y aprobar** esta especificación
2. **Crear branch** `feature/fase-2-diferenciacion`
3. **Iniciar Sprint 1**: Auto-Optimización
4. **Review semanal** de progreso
5. **Demo** al finalizar cada Sprint
6. **Release v2.0** al completar Fase 2

---

## Notas Finales

### Consideraciones Importantes
1. **Validación es crítica**: El código generado debe ser 100% válido
2. **Performance**: Grafo con 1000+ medidas debe renderizar <5s
3. **UX**: Las optimizaciones deben ser entendibles sin conocimiento técnico profundo
4. **Extensibilidad**: Diseño modular para agregar más tipos de optimización

### Riesgos Identificados
1. **Complejidad de parsing DAX**: Algunos casos edge pueden fallar
2. **Performance de grafo**: NetworkX puede ser lento con grafos grandes
3. **Estimación de cardinalidad**: Sin metadata real, estimaciones son aproximadas
4. **Validación semántica**: Solo validamos sintaxis, no semántica

### Mitigaciones
1. Manejo robusto de errores + fallback a modo manual
2. Limitar visualización a top N nodos + filtros
3. Permitir usuario ingresar metadata manualmente
4. Disclaimer claro: "Validar en Power BI antes de aplicar"

---

**Desarrollado por:** Adrián Javier Messina
**Fecha:** Febrero 2026
**Versión:** 1.0

---

## Anexo: Ejemplos de Código Real

### Ejemplo 1: Antes y Después de Auto-Optimización

**Antes:**
```dax
Total Ventas Año Anterior =
CALCULATE(
    SUM(Ventas[Monto]),
    FILTER(
        ALL(Calendario),
        Calendario[Año] = YEAR(TODAY()) - 1
    )
) +
CALCULATE(
    SUM(Ventas[Monto]),
    FILTER(
        ALL(Calendario),
        Calendario[Año] = YEAR(TODAY()) - 1
    )
) * 0.1
```

**Después (con variables):**
```dax
Total Ventas Año Anterior =
VAR VentasAnterior =
    CALCULATE(
        SUM(Ventas[Monto]),
        FILTER(
            ALL(Calendario),
            Calendario[Año] = YEAR(TODAY()) - 1
        )
    )
RETURN
    VentasAnterior + (VentasAnterior * 0.1)
```

**Mejora:**
- Score: 85 → 45 (-40 puntos)
- Expresión evaluada 1 vez en lugar de 2
- Más legible y mantenible

---

FIN DEL DOCUMENTO
