# 🚀 Quick Start - Implementación Fase 2

**Para:** Adrián Javier Messina
**Fecha:** Febrero 2026
**Objetivo:** Guía rápida para retomar desarrollo de Fase 2

---

## 📋 Antes de Empezar

### ✅ Checklist Pre-Desarrollo

- [ ] Leer `FASE2_DIFERENCIACION.md` completo
- [ ] Revisar `ROADMAP.md` para contexto general
- [ ] Verificar versión actual funcionando: `streamlit run streamlit_app/app.py`
- [ ] Tener entorno virtual activado
- [ ] Git configurado y sincronizado

### 🛠️ Setup Rápido

```bash
# 1. Activar entorno virtual
cd "C:\Users\SE46958\1 - Claude - Proyecto viz\Dax optimization\dax-optimizer-streamlit-v1.1"
venv\Scripts\activate  # Windows

# 2. Instalar dependencias adicionales
pip install networkx==3.2
pip install python-louvain==0.16
pip install pytest==7.4.3
pip install pydantic==2.5.0

# 3. Crear branch de desarrollo
git checkout -b feature/fase-2-diferenciacion

# 4. Crear estructura de archivos
mkdir -p core/tests
mkdir -p streamlit_app/components
mkdir -p data
```

---

## 🎯 Implementación por Feature

### Feature 1: Auto-Optimización (Semana 1)

#### Día 1-2: Core

**Crear archivo:** `core/dax_optimizer.py`

**Copy-paste inicial:**
```python
"""
Motor de auto-optimización de código DAX
Desarrollado por: Adrián Javier Messina
Fecha: 2026
"""

from dataclasses import dataclass
from typing import List, Tuple
import re

@dataclass
class OptimizationAction:
    """Representa una acción de optimización"""
    id: str
    type: str
    description: str
    original_code: str
    optimized_code: str
    estimated_improvement: str
    validation_result: Tuple[bool, List[str]]


class DaxOptimizer:
    """Motor de optimización de código DAX"""

    def __init__(self):
        self.optimizations = []

    def suggest_optimizations(self, parsed_dax, issues):
        """Genera lista de optimizaciones aplicables"""
        # TODO: Implementar
        pass


def validate_dax_syntax(code: str) -> Tuple[bool, List[str]]:
    """Valida sintaxis básica de código DAX"""
    errors = []

    # Validar paréntesis balanceados
    stack = []
    for char in code:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False, ["Paréntesis desbalanceados"]
            stack.pop()

    if stack:
        errors.append("Paréntesis desbalanceados")

    # Validar VAR/RETURN
    has_var = bool(re.search(r'\bVAR\b', code, re.IGNORECASE))
    has_return = bool(re.search(r'\bRETURN\b', code, re.IGNORECASE))

    if has_var and not has_return:
        errors.append("VAR sin RETURN correspondiente")

    return len(errors) == 0, errors


# Test rápido
if __name__ == "__main__":
    # Test 1: Paréntesis balanceados
    is_valid, errors = validate_dax_syntax("CALCULATE([Ventas], FILTER(...))")
    print(f"Test 1: {is_valid}, {errors}")

    # Test 2: Paréntesis desbalanceados
    is_valid, errors = validate_dax_syntax("CALCULATE([Ventas], FILTER(...)")
    print(f"Test 2: {is_valid}, {errors}")
```

**Ejecutar test:**
```bash
python core/dax_optimizer.py
```

**Siguiente paso:** Implementar `_generate_add_variables()` según especificación en `FASE2_DIFERENCIACION.md` línea 110-140.

#### Día 3-4: UI

**Crear archivo:** `streamlit_app/components/optimization_panel.py`

**Copy-paste inicial:**
```python
"""
Panel de auto-optimización para Streamlit
"""

import streamlit as st
from core.dax_optimizer import DaxOptimizer, validate_dax_syntax


def render_optimization_panel(measure):
    """Renderiza panel de auto-optimización"""

    st.markdown("### ⚙️ Optimización Automática")

    # TODO: Implementar según especificación
    st.info("🚧 En desarrollo...")
```

**Integrar en app principal:**

En `streamlit_app/app.py`, agregar en `render_measure_detail()`:

```python
# Agregar import al inicio
from streamlit_app.components.optimization_panel import render_optimization_panel

# En render_measure_detail(), agregar nuevo tab:
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Código DAX",
    "🔍 Análisis",
    "💡 Sugerencias",
    "📊 Métricas",
    "⚙️ Auto-Optimización"  # NUEVO
])

with tab5:
    render_optimization_panel(measure)
```

#### Día 5: Testing

**Crear archivo:** `core/tests/test_optimizer.py`

```python
import pytest
from core.dax_optimizer import DaxOptimizer, validate_dax_syntax


def test_validate_balanced():
    code = "CALCULATE([A], FILTER(T, T[X] = 1))"
    is_valid, errors = validate_dax_syntax(code)
    assert is_valid == True


def test_validate_unbalanced():
    code = "CALCULATE([A], FILTER(T, T[X] = 1)"
    is_valid, errors = validate_dax_syntax(code)
    assert is_valid == False


# Agregar más tests según necesidad
```

**Ejecutar:**
```bash
pytest core/tests/test_optimizer.py -v
```

---

### Feature 2: Grafo de Dependencias (Semana 2-3)

#### Setup Inicial

**Crear archivo:** `core/dependency_analyzer.py`

**Copy-paste inicial:**
```python
"""
Analizador de dependencias entre medidas DAX
Desarrollado por: Adrián Javier Messina
"""

from dataclasses import dataclass
from typing import List, Dict
import networkx as nx
import re


@dataclass
class MeasureNode:
    """Nodo del grafo de dependencias"""
    name: str
    risk_score: int
    dependencies_in: int
    dependencies_out: int
    depth: int
    is_orphan: bool
    is_bottleneck: bool


class DependencyAnalyzer:
    """Analizador de dependencias entre medidas"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.measures_map = {}

    def build_dependency_graph(self, ranked_measures):
        """Construye grafo de dependencias"""
        # TODO: Implementar
        pass


# Test rápido
if __name__ == "__main__":
    print("DependencyAnalyzer cargado correctamente")
```

**Test de NetworkX:**
```bash
python -c "import networkx as nx; G = nx.DiGraph(); G.add_edge('A', 'B'); print(f'Nodes: {G.nodes()}, Edges: {G.edges()}')"
```

**Siguiente paso:** Implementar según especificación en `FASE2_DIFERENCIACION.md` línea 330-450.

---

### Feature 3: Análisis de Cardinalidad (Semana 4)

**Crear archivo:** `core/cardinality_analyzer.py`

```python
"""
Analizador de cardinalidad de operaciones DAX
"""

from dataclasses import dataclass
from typing import List, Dict
import re


@dataclass
class CardinalityEstimate:
    """Estimación de cardinalidad"""
    operation: str
    table: str
    estimated_rows: int
    confidence: str
    level: str


class CardinalityAnalyzer:
    """Analizador de cardinalidad"""

    def __init__(self, model_metadata: Dict):
        self.metadata = model_metadata

    def analyze_expression(self, dax_expression: str):
        """Analiza cardinalidad de expresión DAX"""
        # TODO: Implementar
        pass


# Test
if __name__ == "__main__":
    print("CardinalityAnalyzer cargado correctamente")
```

---

## 🧪 Testing Continuo

### Después de cada implementación:

```bash
# 1. Tests unitarios
pytest core/tests/ -v

# 2. Ejecutar app
streamlit run streamlit_app/app.py

# 3. Probar con archivo real
# Cargar: C:\Users\SE46958\OneDrive - YPF\...\Tablero B2C Ejecutivo Plus.pbip

# 4. Verificar que:
#    - No hay errores en consola
#    - Features nuevas aparecen
#    - Funcionalidad existente sigue funcionando
```

---

## 📝 Workflow de Desarrollo

### Ciclo típico:

```bash
# 1. Asegurarte que estás en branch correcto
git status

# 2. Implementar feature
code core/nuevo_modulo.py  # o VSCode

# 3. Test rápido
python core/nuevo_modulo.py

# 4. Test unitario
pytest core/tests/test_nuevo_modulo.py

# 5. Test en app
streamlit run streamlit_app/app.py

# 6. Commit
git add .
git commit -m "feat: implementar [nombre feature]"

# 7. Push
git push origin feature/fase-2-diferenciacion
```

### Cuando terminas un Sprint:

```bash
# 1. Asegurar todos los tests pasan
pytest core/tests/ -v

# 2. Actualizar CHANGELOG.md
# Agregar entrada con cambios del sprint

# 3. Merge a develop
git checkout develop
git merge feature/fase-2-diferenciacion

# 4. Tag de versión
git tag -a v2.0-alpha -m "Fase 2 Alpha Release"
git push origin develop --tags
```

---

## 🐛 Troubleshooting

### Error: "Module not found: networkx"
```bash
pip install networkx==3.2
```

### Error: "Cannot import DaxOptimizer"
```bash
# Asegurar que __init__.py existe
touch core/__init__.py

# Agregar export en core/__init__.py
echo "from .dax_optimizer import DaxOptimizer" >> core/__init__.py
```

### Error en Streamlit: "Cannot render graph"
```bash
# Verificar que Plotly esté actualizado
pip install --upgrade plotly
```

### Tests fallan
```bash
# Ejecutar con más detalle
pytest core/tests/ -v --tb=short

# Si es error de import:
export PYTHONPATH="${PYTHONPATH}:."  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;.  # Windows
```

---

## 📊 Checklist de Calidad

Antes de dar por terminado cada feature:

- [ ] Código implementado y funcionando
- [ ] Tests unitarios escritos y pasando
- [ ] Documentación de funciones (docstrings)
- [ ] UI integrada y testeada manualmente
- [ ] Sin errores en consola de Streamlit
- [ ] Funciona con archivo PBIP real
- [ ] Código comentado donde sea necesario
- [ ] CHANGELOG.md actualizado

---

## 🎯 Métricas de Progreso

### Sprint 1 (Auto-Optimización)
- [ ] `dax_optimizer.py` creado (100 líneas)
- [ ] Al menos 1 tipo de optimización funciona
- [ ] UI con preview lado a lado
- [ ] 3+ tests unitarios
- [ ] Testeado con 5+ medidas reales

### Sprint 2 (Grafo)
- [ ] `dependency_analyzer.py` creado (200 líneas)
- [ ] Grafo se visualiza correctamente
- [ ] Detecta dependencias circulares
- [ ] UI con filtros interactivos
- [ ] 5+ tests unitarios

### Sprint 3 (Cardinalidad)
- [ ] `cardinality_analyzer.py` creado (100 líneas)
- [ ] Estima cardinalidad de ALL, FILTER, VALUES
- [ ] Genera alertas por nivel
- [ ] UI con gráfico de barras
- [ ] 3+ tests unitarios

---

## 💡 Tips de Productividad

### VS Code Extensions útiles:
- Python
- Pylance
- GitLens
- Better Comments
- Error Lens

### Atajos de teclado:
- `Ctrl+Shift+P` → Command Palette
- `F5` → Debug
- `Ctrl+` ` → Terminal
- `Ctrl+B` → Toggle Sidebar

### Debugging en Streamlit:
```python
# Agregar breakpoints con:
import pdb; pdb.set_trace()

# O usar logging:
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Variable X: {x}")
```

### Git aliases útiles:
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
```

---

## 📚 Recursos de Referencia Rápida

### Mientras desarrollas:

**NetworkX:**
```python
# Crear grafo
G = nx.DiGraph()
G.add_edge('A', 'B')
G.add_node('C', attribute='value')

# Análisis
nx.degree(G, 'A')  # Grado
nx.descendants(G, 'A')  # Descendientes
nx.simple_cycles(G)  # Ciclos
```

**Plotly:**
```python
# Gráfico de red
fig = go.Figure(data=[go.Scatter(...)])
fig.update_layout(title="...")
st.plotly_chart(fig)
```

**Pytest:**
```python
# Assert
assert valor == esperado
assert valor > 0
assert "substring" in texto

# Fixtures
@pytest.fixture
def sample_data():
    return [1, 2, 3]
```

---

## 🎉 ¡Listo para Empezar!

### Próximo paso:
1. **Abrir** `FASE2_DIFERENCIACION.md`
2. **Ir a** "Sprint 1: Auto-Optimización"
3. **Crear** `core/dax_optimizer.py`
4. **Implementar** según especificación
5. **Testear** continuamente
6. **Iterar** hasta completar

### Cuando tengas dudas:
1. Revisar `FASE2_DIFERENCIACION.md` (especificación completa)
2. Revisar `ROADMAP.md` (visión general)
3. Revisar código existente en `core/` (patrones)
4. Google/StackOverflow (comunidad)

### Cuando termines:
1. Actualizar `CHANGELOG.md`
2. Hacer PR a `develop`
3. Celebrar! 🎉
4. Iniciar siguiente feature

---

**¡Mucha suerte en la implementación!**

Desarrollado por: Adrián Javier Messina
Fecha: Febrero 2026

---

## Contacto de Soporte

Si necesitas ayuda durante la implementación:
- Revisar documentación técnica
- Buscar en issues de GitHub de librerías
- Comunidad de Streamlit
- Stack Overflow para Python/Pandas

---

FIN - QUICK START FASE 2
