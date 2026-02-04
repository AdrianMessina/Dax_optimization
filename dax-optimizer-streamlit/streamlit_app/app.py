"""
DAX Optimizer - Aplicación Streamlit
Analiza y optimiza código DAX para mejor performance
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    parse_dax_code,
    analyze_dax,
    generate_suggestions,
    calculate_score
)

# Configuración de la página
st.set_page_config(
    page_title="DAX Optimizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .issue-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .issue-card.critical {
        border-left: 4px solid #dc3545;
    }
    .issue-card.warning {
        border-left: 4px solid #ffc107;
    }
    .issue-card.info {
        border-left: 4px solid #17a2b8;
    }
    .severity-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    .severity-badge.critical {
        background-color: #dc3545;
        color: white;
    }
    .severity-badge.warning {
        background-color: #ffc107;
        color: black;
    }
    .severity-badge.info {
        background-color: #17a2b8;
        color: white;
    }
    .category-badge {
        background-color: #e9ecef;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        color: #495057;
    }
    .code-snippet {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #667eea;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        margin: 1rem 0;
        white-space: pre-wrap;
        overflow-x: auto;
    }
    .suggestion-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
    }
    .impact-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .impact-badge.high {
        background-color: #28a745;
        color: white;
    }
    .impact-badge.medium {
        background-color: #ffc107;
        color: black;
    }
    .impact-badge.low {
        background-color: #6c757d;
        color: white;
    }
    .success-message {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
    }
    .success-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .code-comparison {
        display: grid;
        gap: 1rem;
        margin: 1rem 0;
    }
    .analyze-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)


# Código de ejemplo
EXAMPLE_DAX = """Total Sales =
SUMX(
    Sales,
    CALCULATE(
        SUMX(
            FILTER(
                Products,
                Products[Category] = "Electronics"
            ),
            Products[Price]
        )
    )
)"""


def get_score_color(score: int) -> str:
    """Retorna el color según el score"""
    if score >= 80:
        return '#22c55e'
    elif score >= 60:
        return '#eab308'
    elif score >= 40:
        return '#f97316'
    else:
        return '#ef4444'


def get_object_type_label(object_type: str) -> str:
    """Retorna la etiqueta en español del tipo de objeto"""
    labels = {
        'measure': 'Medida',
        'calculated-column': 'Columna Calculada',
        'calculated-table': 'Tabla Calculada'
    }
    return labels.get(object_type, object_type)


def create_score_gauge(score: int) -> go.Figure:
    """Crea un gráfico gauge para el score"""
    color = get_score_color(score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Score de Performance", 'font': {'size': 20}},
        number={'suffix': "/100", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#fee'},
                {'range': [40, 60], 'color': '#ffeaa7'},
                {'range': [60, 80], 'color': '#dfe6e9'},
                {'range': [80, 100], 'color': '#d5f4e6'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="white",
        font={'color': "darkgray", 'family': "Arial"}
    )

    return fig


# Header principal
st.markdown("""
    <div class="main-header">
        <h1>⚡ DAX Optimizer</h1>
        <p>Analiza y optimiza tu código DAX para mejor performance</p>
    </div>
""", unsafe_allow_html=True)

# Inicializar session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# Editor de código
st.markdown("### 📝 Tu código DAX")

dax_code = st.text_area(
    "Pega tu código DAX aquí",
    value=EXAMPLE_DAX,
    height=300,
    help="Escribe o pega tu código DAX para analizar"
)

# Botón de análisis
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("🔍 Analizar Código", use_container_width=True, type="primary"):
        if dax_code.strip():
            # Parsear código
            parsed = parse_dax_code(dax_code)

            # Analizar
            issues, metrics = analyze_dax(parsed)

            # Generar sugerencias
            suggestions = generate_suggestions(parsed, issues)

            # Calcular score
            score = calculate_score(parsed, issues)

            # Guardar resultado
            st.session_state.analysis_result = {
                'parsed': parsed,
                'issues': issues,
                'metrics': metrics,
                'suggestions': suggestions,
                'score': score
            }
            st.rerun()
        else:
            st.warning("Por favor, ingresa código DAX para analizar")

with col2:
    if st.button("🗑️ Limpiar", use_container_width=True):
        st.session_state.analysis_result = None
        st.rerun()

# Mostrar resultados si existen
if st.session_state.analysis_result:
    result = st.session_state.analysis_result

    st.markdown("---")
    st.markdown("## 📊 Resultados del Análisis")

    # Score y tipo de objeto
    col1, col2 = st.columns([1, 2])

    with col1:
        fig = create_score_gauge(result['score'])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <p style="font-size: 1.1rem; color: #666;">
                    Tipo: <strong>{get_object_type_label(result['parsed'].object_type)}</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📈 Métricas de Performance")

        metrics = result['metrics']

        # Grid de métricas
        metric_cols = st.columns(4)

        with metric_cols[0]:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics.complexity}</div>
                    <div class="metric-label">Complejidad</div>
                </div>
            """, unsafe_allow_html=True)

        with metric_cols[1]:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics.nested_iterators}</div>
                    <div class="metric-label">Iteradores Anidados</div>
                </div>
            """, unsafe_allow_html=True)

        with metric_cols[2]:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics.context_transitions}</div>
                    <div class="metric-label">Context Transitions</div>
                </div>
            """, unsafe_allow_html=True)

        with metric_cols[3]:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics.variables_used}</div>
                    <div class="metric-label">Variables Usadas</div>
                </div>
            """, unsafe_allow_html=True)

    # Problemas detectados
    if result['issues']:
        st.markdown("---")
        st.markdown(f"### 🔴 Problemas Detectados ({len(result['issues'])})")

        for issue in result['issues']:
            severity_icon = {'critical': '🔴', 'warning': '🟡', 'info': 'ℹ️'}[issue.severity]

            st.markdown(f"""
                <div class="issue-card {issue.severity}">
                    <div style="margin-bottom: 1rem;">
                        <span class="severity-badge {issue.severity}">
                            {severity_icon} {issue.severity.upper()}
                        </span>
                        <span class="category-badge">{issue.category}</span>
                    </div>
                    <h4 style="margin: 0.5rem 0;">{issue.title}</h4>
                    <p style="color: #666;">{issue.description}</p>
                    {f'<div class="code-snippet">{issue.snippet}</div>' if issue.snippet else ''}
                    {f'<a href="{issue.learn_more}" target="_blank" style="color: #667eea; text-decoration: none;">Aprende más →</a>' if issue.learn_more else ''}
                </div>
            """, unsafe_allow_html=True)

    # Sugerencias de optimización
    if result['suggestions']:
        st.markdown("---")
        st.markdown(f"### 💡 Sugerencias de Optimización ({len(result['suggestions'])})")

        for suggestion in result['suggestions']:
            impact_labels = {'high': 'Alto', 'medium': 'Medio', 'low': 'Bajo'}

            st.markdown(f"""
                <div class="suggestion-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0;">{suggestion.title}</h4>
                        <span class="impact-badge {suggestion.impact}">
                            Impacto: {impact_labels[suggestion.impact]}
                        </span>
                    </div>
                    <p style="color: #666; margin-bottom: 1rem;">{suggestion.description}</p>
                    <div class="code-comparison">
                        <div class="code-snippet">{suggestion.suggested_code}</div>
                    </div>
                    <p style="margin-top: 1rem;">
                        <strong>Por qué:</strong> {suggestion.reason}
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # Mensaje de éxito si no hay problemas
    if not result['issues']:
        st.markdown("""
            <div class="success-message">
                <div class="success-icon">✅</div>
                <h3>¡Excelente trabajo!</h3>
                <p>No se detectaron problemas de performance obvios en tu código DAX.</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>DAX Optimizer | Herramienta de análisis y optimización de código DAX para Power BI</p>
        <p style="font-size: 0.9rem;">Desarrollado con ❤️ usando Streamlit</p>
    </div>
""", unsafe_allow_html=True)
