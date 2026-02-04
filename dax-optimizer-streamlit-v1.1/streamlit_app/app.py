"""
DAX Optimizer v1.1 - Streamlit Application
Análisis completo de archivos PBIP con ranking de medidas
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import os
import time

# Streamlit extras para componentes visuales mejorados (OPCIONAL)
try:
    from streamlit_extras.metric_cards import style_metric_cards
    from streamlit_extras.colored_header import colored_header
    STREAMLIT_EXTRAS_AVAILABLE = True
except ImportError:
    STREAMLIT_EXTRAS_AVAILABLE = False
    # Fallback: crear funciones dummy
    def style_metric_cards(*args, **kwargs):
        pass
    def colored_header(label, description="", color_name="blue-70"):
        st.markdown(f'<h1 class="main-header">{label}</h1>', unsafe_allow_html=True)
        if description:
            st.markdown(f'<p class="sub-header">{description}</p>', unsafe_allow_html=True)

# Streamlit Lottie para animaciones profesionales (OPCIONAL)
try:
    from streamlit_lottie import st_lottie
    import requests
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# Agregar path del core module
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    extract_measures_from_pbip,
    validate_pbip_file,
    get_pbip_info,
    parse_dax_code,
    analyze_dax,
    generate_suggestions,
    calculate_score,
    rank_measures,
    get_summary_stats,
    filter_measures_by_priority,
    get_top_issues,
    get_priority_color
)


# Configuración de página con ícono personalizado
icon_path = Path(__file__).parent / "assets" / "dax_optimization.ico"
st.set_page_config(
    page_title="DAX Optimizer v1.1",
    page_icon=str(icon_path) if icon_path.exists() else "⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Estilos CSS personalizados basados en el ícono de la aplicación - MEJORADOS
st.markdown("""
<style>
    /* ============================================
       ANIMACIONES Y KEYFRAMES
       ============================================ */

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideInFromLeft {
        0% { transform: translateX(-30px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }

    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }

    /* ============================================
       HEADERS Y TÍTULOS
       ============================================ */

    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(120deg, #0066cc 0%, #00b4d8 50%, #48cae4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: fadeIn 0.8s ease-out;
        text-shadow: 0 4px 6px rgba(0, 102, 204, 0.1);
    }

    .sub-header {
        text-align: center;
        color: #495057;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-out;
    }

    /* ============================================
       METRIC CARDS CON GLASSMORPHISM
       ============================================ */

    .metric-card {
        background: linear-gradient(135deg, #0066cc 0%, #0096c7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 102, 204, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 24px rgba(0, 102, 204, 0.3);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* ============================================
       BADGES CON EFECTOS MODERNOS
       ============================================ */

    .issue-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .issue-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    .critical-badge {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
    }

    .warning-badge {
        background: linear-gradient(135deg, #fd7e14 0%, #e8590c 100%);
        color: white;
    }

    .info-badge {
        background: linear-gradient(135deg, #0066cc 0%, #0056b3 100%);
        color: white;
    }

    /* ============================================
       EXPANDERS CON GLASSMORPHISM
       ============================================ */

    .stExpander {
        background: rgba(248, 249, 250, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(233, 236, 239, 0.8);
        transition: all 0.3s ease;
    }

    .stExpander:hover {
        background: rgba(248, 249, 250, 0.95);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* ============================================
       MEASURE CARDS MEJORADOS
       ============================================ */

    .measure-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.08);
        border-left: 6px solid #0066cc;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: slideInFromLeft 0.5s ease-out;
    }

    .measure-card::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.02));
        pointer-events: none;
    }

    .measure-card:hover {
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.15);
        transform: translateY(-4px) translateX(4px);
        border-left-width: 8px;
    }

    /* ============================================
       DEVELOPER BADGE CON EFECTOS
       ============================================ */

    .developer-badge {
        background: linear-gradient(135deg, #0066cc 0%, #00b4d8 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .developer-badge::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: float 3s ease-in-out infinite;
    }

    .developer-badge:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(0, 102, 204, 0.3);
    }

    /* ============================================
       HOW IT WORKS BOX MEJORADO
       ============================================ */

    .how-it-works-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #0066cc;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.1);
        transition: all 0.3s ease;
    }

    .how-it-works-box:hover {
        box-shadow: 0 4px 16px rgba(0, 102, 204, 0.15);
        transform: translateX(5px);
    }

    /* ============================================
       BOTONES MEJORADOS
       ============================================ */

    .stButton>button {
        background: linear-gradient(135deg, #0066cc 0%, #0096c7 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.2);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #0056b3 0%, #007bbd 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 102, 204, 0.3);
    }

    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }

    /* ============================================
       INPUTS MEJORADOS
       ============================================ */

    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
    }

    /* ============================================
       SLIDERS MEJORADOS
       ============================================ */

    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #0066cc 0%, #00b4d8 100%);
    }

    /* ============================================
       METRICS DE STREAMLIT MEJORADOS
       ============================================ */

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(120deg, #0066cc 0%, #00b4d8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* ============================================
       SKELETON LOADER (Para uso futuro)
       ============================================ */

    .skeleton {
        animation: shimmer 2s infinite;
        background: linear-gradient(
            to right,
            #f0f0f0 0%,
            #e0e0e0 20%,
            #f0f0f0 40%,
            #f0f0f0 100%
        );
        background-size: 1000px 100%;
        border-radius: 8px;
        height: 20px;
        margin-bottom: 10px;
    }

    /* ============================================
       SCROLL PERSONALIZADO
       ============================================ */

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0066cc 0%, #00b4d8 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0056b3 0%, #0096c7 100%);
    }

    /* ============================================
       TABLAS MEJORADAS
       ============================================ */

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* ============================================
       TOOLTIPS MEJORADOS
       ============================================ */

    [data-testid="stTooltipIcon"] {
        color: #0066cc;
        transition: all 0.3s ease;
    }

    [data-testid="stTooltipIcon"]:hover {
        color: #00b4d8;
        transform: scale(1.2);
    }

    /* ============================================
       EFECTOS GENERALES DE PÁGINA
       ============================================ */

    .main .block-container {
        animation: fadeIn 0.6s ease-out;
    }

    /* ============================================
       CÓDIGO BLOCKS MEJORADOS
       ============================================ */

    .stCodeBlock {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* ============================================
       ALERTS MEJORADOS
       ============================================ */

    .stAlert {
        border-radius: 12px;
        border-left-width: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        animation: slideInFromLeft 0.4s ease-out;
    }

    /* ============================================
       PROGRESS BARS MEJORADOS
       ============================================ */

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0066cc 0%, #00b4d8 50%, #48cae4 100%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
</style>
""", unsafe_allow_html=True)


def load_lottie_url(url: str):
    """Carga una animación Lottie desde una URL de manera segura"""
    if not LOTTIE_AVAILABLE:
        return None
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def show_lottie_animation(lottie_json, height=200, key="lottie"):
    """Muestra una animación Lottie si está disponible"""
    if LOTTIE_AVAILABLE and lottie_json is not None:
        st_lottie(lottie_json, height=height, key=key)


def render_header():
    """Renderiza el header de la aplicación"""
    col_logo, col_title = st.columns([1, 9])

    with col_logo:
        icon_path = Path(__file__).parent / "assets" / "dax_optimization.ico"
        if icon_path.exists():
            st.image(str(icon_path), width=80)
        else:
            st.markdown('<p style="font-size: 4rem;">⚡</p>', unsafe_allow_html=True)

    with col_title:
        # Usar colored_header para un header más moderno
        colored_header(
            label="DAX Optimizer v1.1",
            description="Análisis avanzado de medidas DAX con sistema de tolerancia",
            color_name="blue-70"
        )

    # Cómo funciona en el header
    with st.expander("📖 ¿Cómo funciona?", expanded=False):
        st.markdown("""
        <div class="how-it-works-box">

        ### 🔄 Proceso de análisis:

        1. **📁 Carga del archivo PBIP**: Se extraen todas las medidas DAX del modelo
        2. **🔍 Análisis individual**: Cada medida se analiza en busca de:
           - Problemas críticos de performance
           - Advertencias de mejores prácticas
           - Oportunidades de optimización
        3. **📊 Cálculo de scores**: Se asigna un score de 0-100 a cada medida
        4. **📈 Ranking y priorización**: Las medidas se ordenan por impacto
        5. **💡 Recomendaciones**: Se generan sugerencias específicas de optimización

        ### 📏 Criterios de evaluación (Score de Riesgo):

        - 🔴 **Crítico (76-100)**: Problemas severos que afectan significativamente la performance
        - 🟠 **Alto (51-75)**: Múltiples warnings o complejidad alta
        - 🟡 **Medio (26-50)**: Algunos problemas menores
        - 🟢 **Bajo (0-25)**: Código bien optimizado

        **📌 Nota:** Mayor score = Mayor riesgo de impacto en performance

        </div>
        """, unsafe_allow_html=True)


def render_file_upload():
    """Renderiza la sección de carga de archivo o carpeta PBIP"""
    with st.expander("📁 Cargar archivo PBIP", expanded=True):
        st.info("""
        **ℹ️ Estructura de archivos PBIP:**

        Cuando guardas un archivo como PBIP en Power BI Desktop, se generan:
        - 📄 Un archivo `.pbip` (archivo de configuración JSON)
        - 📁 Una carpeta `.SemanticModel` (contiene el modelo de datos)
        - 📁 Una carpeta `.Report` (contiene el reporte)

        **Puedes pegar la ruta a cualquiera de estos:**
        1. La ruta al archivo `.pbip` (Ejemplo: `C:\\Users\\...\\MiReporte.pbip`)
        2. La ruta a la carpeta `.SemanticModel` (Ejemplo: `C:\\Users\\...\\MiReporte.SemanticModel`)
        3. La ruta a la carpeta padre que contiene todo
        """)

        # Opción 1: Ruta a archivo/carpeta PBIP (recomendado)
        st.markdown("**Opción 1: Pegar ruta** (Recomendado)")
        pbip_folder_path = st.text_input(
            "Pega la ruta completa al archivo .pbip o a la carpeta .SemanticModel",
            placeholder=r"C:\Users\...\MiReporte.pbip",
            help="Copia y pega la ruta completa al archivo .pbip. ✅ Puedes pegar la ruta CON comillas, la aplicación las detecta automáticamente."
        )

        # Nota sobre comillas
        st.success("✅ **Nota importante:** Si al copiar la ruta esta incluye comillas (como `\"C:\\Users\\...\\archivo.pbip\"`), ¡no te preocupes! La aplicación las reconoce y procesa correctamente.")

        # Mostrar instrucciones de cómo copiar la ruta
        with st.expander("💡 ¿Cómo copiar la ruta del archivo?"):
            st.markdown("""
            **Opción A: Desde el Explorador de Windows**
            1. Abre el Explorador de Windows
            2. Navega hasta la carpeta que contiene tu archivo `.pbip`
            3. **SHIFT + Click derecho** en el archivo `.pbip` → **Copiar como ruta de acceso**
            4. Pega la ruta arriba ✅ **(se copiará con comillas, la app las procesa automáticamente)**

            **Opción B: Desde la barra de direcciones**
            1. Abre el Explorador de Windows
            2. Navega hasta la carpeta que contiene tu archivo `.pbip`
            3. Click en la barra de direcciones arriba → Copiar
            4. Pega la ruta arriba y agrega `\\NombreDeArchivo.pbip` al final

            **Ejemplo de ruta válida:**
            ```
            C:\\Users\\TuUsuario\\Documentos\\MiProyecto\\Reporte.pbip
            ```
            O con comillas:
            ```
            "C:\\Users\\TuUsuario\\Documentos\\MiProyecto\\Reporte.pbip"
            ```
            """)

        # Opción 2: Archivo ZIP (alternativa)
        st.markdown("**Opción 2: Subir archivo ZIP** (Alternativa)")
        uploaded_file = st.file_uploader(
            "O selecciona un archivo .zip si comprimiste el PBIP",
            type=['zip'],
            help="Si comprimiste todas las carpetas PBIP en un archivo ZIP, súbelo aquí"
        )

    return pbip_folder_path, uploaded_file


def export_measures_to_csv(ranked_measures):
    """Exporta las medidas analizadas a un archivo CSV"""
    data = []
    for measure in ranked_measures:
        row = {
            'Nombre': measure.name,
            'Tabla': measure.table,
            'Score de Riesgo': measure.impact_score,
            'Prioridad': measure.priority_label,
            'Complejidad': measure.complexity,
            'Issues Críticos': measure.critical_issues,
            'Warnings': measure.warnings,
            'Total Issues': measure.critical_issues + measure.warnings,
            'Funciones': measure.metrics.function_count if measure.metrics else 0,
            'Variables': measure.metrics.variables_used if measure.metrics else 0,
            'Iteradores Anidados': measure.metrics.nested_iterators if measure.metrics else 0,
            'Transiciones de Contexto': measure.metrics.context_transitions if measure.metrics else 0,
            'Impacto Estimado': measure.metrics.estimated_impact if measure.metrics else 'N/A',
            'Expresión DAX': measure.expression
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode('utf-8')


def export_measures_to_html(ranked_measures):
    """Exporta las medidas analizadas a un archivo HTML con formato"""
    data = []
    for measure in ranked_measures:
        row = {
            'Nombre': measure.name,
            'Tabla': measure.table,
            'Score de Riesgo': measure.impact_score,
            'Prioridad': measure.priority_label,
            'Complejidad': measure.complexity,
            'Issues Críticos': measure.critical_issues,
            'Warnings': measure.warnings,
            'Total Issues': measure.critical_issues + measure.warnings,
            'Funciones': measure.metrics.function_count if measure.metrics else 0,
            'Variables': measure.metrics.variables_used if measure.metrics else 0,
            'Iteradores Anidados': measure.metrics.nested_iterators if measure.metrics else 0,
            'Transiciones de Contexto': measure.metrics.context_transitions if measure.metrics else 0,
            'Impacto Estimado': measure.metrics.estimated_impact if measure.metrics else 'N/A'
        }
        data.append(row)

    df = pd.DataFrame(data)

    # Crear HTML con estilos
    html = df.to_html(index=False, escape=False, classes='table table-striped')

    # Agregar estilos CSS
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Análisis DAX - Reporte</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
            h1 {{ color: #0066cc; }}
            .table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .table th {{ background: #0066cc; color: white; padding: 12px; text-align: left; }}
            .table td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
            .table tr:hover {{ background: #f1f3f5; }}
        </style>
    </head>
    <body>
        <h1>⚡ DAX Optimizer - Análisis de Medidas</h1>
        <p>Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        {html}
    </body>
    </html>
    """

    return styled_html.encode('utf-8')


def render_summary_stats(stats: dict, tolerance: int = 50):
    """Renderiza estadísticas de resumen con score de tolerancia"""
    st.markdown("### 📊 Resumen del análisis")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total de medidas", stats['total_measures'])

    with col2:
        st.metric("🔴 Riesgo crítico", stats['critical_measures'],
                 delta=None, delta_color="inverse")

    with col3:
        st.metric("🟠 Riesgo alto", stats['high_priority'],
                 delta=None, delta_color="inverse")

    with col4:
        st.metric("Issues críticos", stats['total_critical_issues'])

    with col5:
        # Comparar con tolerancia
        avg_score = stats['avg_score']
        delta = avg_score - tolerance
        delta_color = "inverse"  # Rojo si es positivo (por encima de tolerancia)

        if avg_score > tolerance:
            help_text = f"⚠️ El reporte está {delta:.1f} puntos por encima de la tolerancia"
        else:
            help_text = f"✅ El reporte está dentro de la tolerancia ({tolerance} puntos)"

        st.metric("Riesgo promedio", f"{avg_score:.1f}/100",
                 delta=f"{delta:+.1f} vs tolerancia",
                 delta_color=delta_color,
                 help=help_text)

    # Aplicar estilo mejorado a todas las métricas
    style_metric_cards(
        background_color="#FFFFFF",
        border_left_color="#0066cc",
        border_color="#e9ecef",
        box_shadow=True,
        border_size_px=2,
        border_radius_px=12
    )


def render_tolerance_gauge(avg_score: float, tolerance: int):
    """Renderiza un gauge mostrando el score promedio vs tolerancia"""
    # Determinar color según si está dentro o fuera de tolerancia
    if avg_score <= tolerance * 0.5:
        gauge_color = "#2ed573"  # Verde
    elif avg_score <= tolerance:
        gauge_color = "#ffd32a"  # Amarillo
    elif avg_score <= tolerance * 1.5:
        gauge_color = "#ffa502"  # Naranja
    else:
        gauge_color = "#ff4757"  # Rojo

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Score Promedio del Reporte", 'font': {'size': 18}},
        delta={'reference': tolerance, 'increasing': {'color': "#ff4757"}, 'decreasing': {'color': "#2ed573"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': gauge_color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, tolerance], 'color': 'rgba(46, 213, 115, 0.2)'},
                {'range': [tolerance, 100], 'color': 'rgba(255, 71, 87, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': tolerance
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        font={'color': "darkgray", 'family': "Arial"}
    )

    return fig


def render_top_risky_measures_with_influence(ranked_measures, tolerance: int, top_n=10):
    """Renderiza gráfico de top medidas mostrando su influencia en el score total"""
    # Tomar las top N medidas con mayor riesgo
    top_measures = ranked_measures[:top_n]

    if not top_measures:
        return None

    # Calcular score total y contribución de cada medida
    total_measures = len(ranked_measures)
    avg_score = sum(m.impact_score for m in ranked_measures) / total_measures

    # Preparar datos
    names = [m.name[:35] + '...' if len(m.name) > 35 else m.name for m in top_measures]
    scores = [m.impact_score for m in top_measures]
    # Contribución: cuánto aporta esta medida al score promedio
    contributions = [(m.impact_score / total_measures) for m in top_measures]
    colors = [get_priority_color(m.impact_score) for m in top_measures]

    # Crear gráfico de barras horizontales
    fig = go.Figure()

    # Barra principal de score
    fig.add_trace(go.Bar(
        y=names[::-1],
        x=scores[::-1],
        orientation='h',
        name='Score de Riesgo',
        marker=dict(
            color=colors[::-1],
            line=dict(color='rgba(0,0,0,0.3)', width=1)
        ),
        text=[f"{s:.0f}" for s in scores[::-1]],
        textposition='inside',
        textfont=dict(color='white', size=12, family='Arial Black'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}/100<br>Contribución al promedio: %{customdata:.2f}<extra></extra>',
        customdata=contributions[::-1]
    ))

    # Línea de tolerancia
    fig.add_vline(
        x=tolerance,
        line_dash="dash",
        line_color="red",
        line_width=3,
        annotation_text=f"Tolerancia ({tolerance})",
        annotation_position="top"
    )

    # Línea de score promedio
    fig.add_vline(
        x=avg_score,
        line_dash="dot",
        line_color="blue",
        line_width=2,
        annotation_text=f"Promedio ({avg_score:.1f})",
        annotation_position="bottom"
    )

    fig.update_layout(
        title=f"Top {top_n} Medidas con Mayor Riesgo e Influencia",
        xaxis_title="Score de Riesgo (0-100)",
        yaxis_title="",
        height=450,
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[0, 100],
            gridcolor='rgba(128,128,128,0.2)'
        ),
        font=dict(size=11)
    )

    return fig


def render_top_issues(ranked_measures):
    """Renderiza los issues más comunes"""
    top_issues = get_top_issues(ranked_measures, top_n=5)

    if not top_issues:
        return

    st.markdown("### 🎯 Issues más frecuentes")

    for idx, issue in enumerate(top_issues, 1):
        severity_colors = {
            'critical': '🔴',
            'warning': '⚠️',
            'info': 'ℹ️'
        }

        icon = severity_colors.get(issue['severity'], '•')

        with st.expander(f"{icon} **{issue['title']}** - Encontrado en {issue['count']} medida(s)"):
            st.write(f"**ID:** `{issue['id']}`")
            st.write(f"**Severidad:** {issue['severity'].upper()}")
            st.write(f"**Medidas afectadas:** {', '.join(issue['measures'][:5])}")
            if len(issue['measures']) > 5:
                st.write(f"... y {len(issue['measures']) - 5} más")


def render_measures_table(ranked_measures):
    """Renderiza tabla de medidas con ranking"""
    st.markdown("### 📋 Ranking de medidas")

    # Filtros
    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        priority_filter = st.selectbox(
            "Filtrar por prioridad",
            ["Todas", "Crítico", "Alto", "Medio", "Bajo"]
        )

    with col2:
        sort_by = st.selectbox(
            "Ordenar por",
            ["Riesgo (mayor primero)", "Riesgo (menor primero)", "Nombre", "Complejidad"]
        )

    with col3:
        search = st.text_input("🔍 Buscar medida", placeholder="Nombre de la medida...")

    # Aplicar filtros
    filtered_measures = filter_measures_by_priority(ranked_measures, priority_filter)

    if search:
        filtered_measures = [
            m for m in filtered_measures
            if search.lower() in m.name.lower()
        ]

    # Aplicar ordenamiento
    if sort_by == "Riesgo (menor primero)":
        filtered_measures.sort(key=lambda m: m.impact_score)
    elif sort_by == "Nombre":
        filtered_measures.sort(key=lambda m: m.name)
    elif sort_by == "Complejidad":
        filtered_measures.sort(key=lambda m: m.complexity, reverse=True)
    # Por defecto ya está ordenado por riesgo (mayor primero)

    st.markdown(f"**Mostrando {len(filtered_measures)} de {len(ranked_measures)} medidas**")

    # Renderizar tabla
    for idx, measure in enumerate(filtered_measures):
        render_measure_row(measure, idx)


def render_measure_row(measure, index):
    """Renderiza una fila de medida expandible con diseño mejorado"""

    # Color según prioridad
    border_color = get_priority_color(measure.impact_score)

    # Emoji según prioridad
    priority_emoji = {
        "Crítico": "🔴",
        "Alto": "🟠",
        "Medio": "🟡",
        "Bajo": "🟢"
    }
    emoji = priority_emoji.get(measure.priority_label, "⚪")

    # Contenedor de la medida con diseño mejorado
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0, 102, 204, 0.15);
                border-left: 6px solid {border_color};
                border: 1px solid #e9ecef;">
    """, unsafe_allow_html=True)

    # Header con información principal
    col1, col2, col3, col4 = st.columns([4, 1.5, 1, 1])

    with col1:
        st.markdown(f"### {measure.name}")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%);
                    padding: 8px 12px; border-radius: 8px; display: inline-block; margin-top: 5px;">
            📊 Tabla: <strong>{measure.table}</strong>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Badge de prioridad grande y claro
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {border_color} 0%, {border_color}dd 100%);
                    color: white; padding: 12px 18px;
                    border-radius: 25px; text-align: center; font-weight: bold; font-size: 15px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            {emoji} {measure.priority_label.upper()}
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.metric("Score Riesgo", f"{measure.impact_score}/100",
                 help="Score de 0-100. Mayor = Mayor riesgo de performance")

    with col4:
        # Resumen de issues
        total_issues = measure.critical_issues + measure.warnings
        if total_issues > 0:
            st.metric("Issues", total_issues,
                     delta=f"{measure.critical_issues} críticos" if measure.critical_issues > 0 else None,
                     delta_color="inverse")
        else:
            st.metric("Issues", "0", help="Sin problemas detectados")

    # Expander con detalles
    with st.expander("🔍 Ver análisis completo de la medida"):
        render_measure_detail(measure)

    st.markdown("</div>", unsafe_allow_html=True)


def render_measure_detail(measure):
    """Renderiza el análisis detallado de una medida"""

    # Tabs para organizar información
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Código DAX", "🔍 Análisis", "💡 Sugerencias", "📊 Métricas"])

    with tab1:
        st.markdown("#### Código completo")
        st.code(measure.expression, language='dax')

    with tab2:
        st.markdown("#### Problemas detectados")

        if not measure.issues:
            st.success("✅ No se detectaron problemas en esta medida")
        else:
            # Agrupar por severidad
            critical = [i for i in measure.issues if i.severity == 'critical']
            warnings = [i for i in measure.issues if i.severity == 'warning']
            infos = [i for i in measure.issues if i.severity == 'info']

            if critical:
                st.markdown("##### 🔴 Problemas críticos")
                for issue in critical:
                    render_issue_card(issue)

            if warnings:
                st.markdown("##### ⚠️ Advertencias")
                for issue in warnings:
                    render_issue_card(issue)

            if infos:
                st.markdown("##### ℹ️ Información")
                for issue in infos:
                    render_issue_card(issue)

    with tab3:
        st.markdown("#### Recomendaciones de optimización")

        if not measure.suggestions:
            st.info("No hay sugerencias específicas para esta medida")
        else:
            for suggestion in measure.suggestions:
                render_suggestion_card(suggestion)

    with tab4:
        st.markdown("#### Métricas de performance")

        if measure.metrics is not None:
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Complejidad", measure.metrics.complexity)
                st.metric("Funciones totales", measure.metrics.function_count)
                st.metric("Variables usadas", measure.metrics.variables_used)

            with col2:
                st.metric("Iteradores anidados", measure.metrics.nested_iterators)
                st.metric("Transiciones de contexto", measure.metrics.context_transitions)
                st.metric("Impacto estimado", measure.metrics.estimated_impact.upper())
        else:
            st.warning("⚠️ No se pudieron calcular las métricas de performance para esta medida debido a un error en el análisis.")


def render_issue_card(issue):
    """Renderiza una tarjeta de issue"""
    severity_icons = {
        'critical': '🔴',
        'warning': '⚠️',
        'info': 'ℹ️'
    }

    icon = severity_icons.get(issue.severity, '•')

    with st.container():
        st.markdown(f"**{icon} {issue.title}**")
        st.write(issue.description)

        if issue.snippet:
            st.code(issue.snippet, language='dax')

        if issue.learn_more:
            st.markdown(f"[📚 Más información]({issue.learn_more})")

        st.markdown("---")


def render_suggestion_card(suggestion):
    """Renderiza una tarjeta de sugerencia"""
    impact_icons = {
        'high': '🔥',
        'medium': '💡',
        'low': 'ℹ️'
    }

    icon = impact_icons.get(suggestion.impact, '•')

    with st.container():
        st.markdown(f"**{icon} {suggestion.title}** - Impacto: {suggestion.impact.upper()}")
        st.write(suggestion.description)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**❌ Código actual:**")
            st.code(suggestion.original_code, language='dax')

        with col2:
            st.markdown("**✅ Código sugerido:**")
            st.code(suggestion.suggested_code, language='dax')

        st.info(f"**Por qué:** {suggestion.reason}")
        st.markdown("---")


def analyze_pbip_file(file_path: str):
    """Analiza un archivo PBIP completo con animación de progreso"""

    # Animación Lottie de inicio (si está disponible)
    lottie_analyzing = load_lottie_url("https://lottie.host/92769a14-9afe-4f06-b9a1-dfb8c16d88ab/IcWLmUNs9c.json")

    # Animación de inicio
    if lottie_analyzing:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            show_lottie_animation(lottie_analyzing, height=150, key="analyzing_start")

    with st.spinner("🔄 Iniciando análisis del archivo PBIP..."):
        time.sleep(0.5)  # Pequeño delay para dar sensación de análisis

    # Validar archivo
    is_valid, message = validate_pbip_file(file_path)

    if not is_valid:
        st.error(f"❌ Error: {message}")
        return None

    # Mostrar información del archivo
    with st.spinner("📂 Extrayendo información del archivo PBIP..."):
        pbip_info = get_pbip_info(file_path)
        time.sleep(0.5)

    st.success(f"✅ Archivo válido: {pbip_info['format']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tablas", pbip_info['tables_count'])
    with col2:
        st.metric("Medidas encontradas", pbip_info['measures_count'])
    with col3:
        file_size_mb = pbip_info['file_size'] / (1024 * 1024)
        st.metric("Tamaño", f"{file_size_mb:.2f} MB")

    # Extraer medidas
    with st.spinner("🔍 Extrayendo medidas DAX del modelo..."):
        measures = extract_measures_from_pbip(file_path)
        time.sleep(0.5)

    if not measures:
        st.warning("⚠️ No se encontraron medidas en el archivo PBIP")
        return None

    st.info(f"✅ Se encontraron {len(measures)} medidas para analizar")

    # Analizar cada medida
    analyzed_measures = []
    failed_measures = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, measure in enumerate(measures):
        status_text.text(f"Analizando medida {idx + 1} de {len(measures)}: {measure['name']}")

        try:
            # Parsear y analizar
            parsed = parse_dax_code(measure['expression'])
            issues, metrics = analyze_dax(parsed)
            suggestions = generate_suggestions(parsed, issues)
            base_score = calculate_score(parsed, issues)

            analyzed_measures.append({
                'name': measure['name'],
                'table': measure['table'],
                'expression': measure['expression'],
                'issues': issues,
                'metrics': metrics,
                'suggestions': suggestions,
                'base_score': base_score
            })
        except Exception as e:
            # Si falla el análisis de una medida, registrarla y continuar
            failed_measures.append({
                'name': measure['name'],
                'table': measure['table'],
                'error': str(e)
            })

            # Agregar una entrada básica para que al menos aparezca en el reporte
            analyzed_measures.append({
                'name': measure['name'],
                'table': measure['table'],
                'expression': measure['expression'],
                'issues': [],
                'metrics': None,
                'suggestions': [],
                'base_score': 100  # Score neutral para medidas que no se pudieron analizar
            })

        progress_bar.progress((idx + 1) / len(measures))

    progress_bar.empty()
    status_text.empty()

    # Mostrar advertencia si hubo medidas que fallaron
    if failed_measures:
        with st.expander(f"⚠️ {len(failed_measures)} medida(s) no se pudieron analizar completamente", expanded=False):
            for failed in failed_measures:
                st.warning(f"**{failed['name']}** (Tabla: {failed['table']}): {failed['error']}")
            st.info("Estas medidas fueron incluidas en el reporte con un score neutral. Puedes revisarlas manualmente.")

    # Rankear medidas con animación
    with st.spinner("📊 Calculando ranking de medidas y generando estadísticas..."):
        ranked_measures = rank_measures(analyzed_measures)
        time.sleep(0.7)

    # Mensaje de éxito con animación
    success_placeholder = st.empty()
    success_placeholder.success("🎉 ¡Análisis completado exitosamente! Los resultados están listos.")
    time.sleep(1.5)
    success_placeholder.empty()

    return ranked_measures


def main():
    """Función principal de la aplicación"""

    # Render header
    render_header()

    # Sidebar con diseño mejorado
    with st.sidebar:
        # Logo/título del sidebar
        st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h2 style="color: #0066cc; margin-bottom: 5px;">⚡ DAX Optimizer</h2>
            <p style="color: #6c757d; font-size: 0.9rem; margin-top: -5px;">v1.1</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Características con iconos mejorados
        with st.expander("✨ Características principales", expanded=True):
            st.markdown("""
            - 📂 **Análisis completo de archivos PBIP**
              Procesa todo tu modelo de datos en segundos

            - 🔍 **Detección inteligente de problemas**
              Identifica issues críticos de performance

            - 📊 **Sistema de scoring con tolerancia**
              Evalúa el riesgo de cada medida DAX

            - 💡 **Sugerencias de optimización**
              Recomendaciones específicas y accionables

            - 📈 **Visualización de influencia**
              Gráficos interactivos para análisis rápido
            """)

        st.markdown("---")

        # Guía rápida
        with st.expander("🚀 Guía rápida"):
            st.markdown("""
            **Paso 1:** Copia la ruta de tu archivo `.pbip`

            **Paso 2:** Pégala en el campo de entrada (con o sin comillas)

            **Paso 3:** Ajusta la tolerancia de riesgo según tus necesidades

            **Paso 4:** Explora las medidas con mayor riesgo

            **Paso 5:** Exporta los resultados para compartir
            """)

        st.markdown("---")

        # Desarrollador con diseño mejorado
        st.markdown("""
        <div class="developer-badge">
            <p style="margin: 0; font-size: 0.85rem; opacity: 0.9;">Desarrollado por</p>
            <h3 style="margin: 5px 0; font-size: 1.3rem;">Adrián Javier Messina</h3>
            <p style="margin: 5px 0; font-size: 1rem; font-weight: 600;">Torre Visualización</p>
            <p style="margin: 5px 0; font-size: 0.8rem; opacity: 0.8;">📅 Enero 2026</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Recursos útiles
        with st.expander("📚 Recursos y documentación"):
            st.markdown("""
            **Patrones DAX:**
            - [SQLBI - DAX Patterns](https://www.sqlbi.com/patterns/)
            - [DAX Guide](https://dax.guide/)

            **Power BI:**
            - [Best Practices](https://docs.microsoft.com/power-bi/)
            - [Performance Tuning](https://docs.microsoft.com/power-bi/guidance/power-bi-optimization)

            **Comunidad:**
            - [Power BI Community](https://community.powerbi.com/)
            """)

        st.markdown("---")

        # Versión
        st.markdown("""
        <div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 8px;">
            <p style="margin: 0; font-size: 0.85rem; color: #6c757d;">Versión</p>
            <code style="font-size: 1rem; color: #0066cc; font-weight: 600;">v1.1.2</code>
            <p style="margin: 5px 0 0 0; font-size: 0.75rem; color: #adb5bd;">Build 2026.02.03</p>
        </div>
        """, unsafe_allow_html=True)

    # Upload de archivo o ruta de carpeta
    pbip_folder_path, uploaded_file = render_file_upload()

    # Determinar qué opción usar
    file_to_analyze = None
    temp_file_path = None

    if pbip_folder_path and pbip_folder_path.strip():
        # Opción 1: Ruta a archivo/carpeta PBIP
        pbip_path = pbip_folder_path.strip()

        # Remover comillas si las hay (común al copiar ruta con Shift+Click derecho)
        if pbip_path.startswith('"') and pbip_path.endswith('"'):
            pbip_path = pbip_path[1:-1]
        elif pbip_path.startswith("'") and pbip_path.endswith("'"):
            pbip_path = pbip_path[1:-1]

        if os.path.exists(pbip_path):
            file_to_analyze = pbip_path
        else:
            st.error(f"⚠️ La ruta '{pbip_path}' no existe. Verifica que la ruta sea correcta.")

    elif uploaded_file is not None:
        # Opción 2: Archivo subido
        temp_file_path = os.path.join(os.getcwd(), uploaded_file.name)
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        file_to_analyze = temp_file_path

    if file_to_analyze:
        try:
            # Analizar archivo
            with st.spinner('Analizando archivo PBIP...'):
                ranked_measures = analyze_pbip_file(file_to_analyze)

            if ranked_measures:
                st.success(f"✅ Análisis completado: {len(ranked_measures)} medidas encontradas")

                # Botones de exportación
                col_export1, col_export2, col_export3 = st.columns([1, 1, 4])

                with col_export1:
                    csv_data = export_measures_to_csv(ranked_measures)
                    st.download_button(
                        label="📥 Exportar CSV",
                        data=csv_data,
                        file_name=f"dax_analysis_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Descargar análisis completo en formato CSV"
                    )

                with col_export2:
                    html_data = export_measures_to_html(ranked_measures)
                    st.download_button(
                        label="📥 Exportar HTML",
                        data=html_data,
                        file_name=f"dax_analysis_{time.strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        help="Descargar análisis completo en formato HTML con estilos"
                    )

                st.markdown("---")

                # Control de tolerancia
                st.markdown("### ⚙️ Configuración de Tolerancia")
                tolerance = st.slider(
                    "Umbral de tolerancia de riesgo",
                    min_value=0,
                    max_value=100,
                    value=50,
                    step=5,
                    help="Define el nivel máximo aceptable de riesgo. Medidas por encima de este valor requieren optimización."
                )

                col_info1, col_info2 = st.columns([2, 1])
                with col_info1:
                    st.info(f"""
                    **Tolerancia configurada: {tolerance} puntos**
                    - Medidas con score ≤ {tolerance}: Dentro de tolerancia ✅
                    - Medidas con score > {tolerance}: Requieren atención ⚠️
                    """)
                with col_info2:
                    # Contar medidas fuera de tolerancia
                    measures_above = sum(1 for m in ranked_measures if m.impact_score > tolerance)
                    st.metric("Medidas fuera de tolerancia",
                             f"{measures_above}/{len(ranked_measures)}",
                             delta=f"{(measures_above/len(ranked_measures)*100):.1f}%",
                             delta_color="inverse")

                st.markdown("---")

                # Estadísticas de resumen
                stats = get_summary_stats(ranked_measures)
                render_summary_stats(stats, tolerance=tolerance)

                st.markdown("---")

                # Visualizaciones
                col1, col2 = st.columns([2, 1])

                with col1:
                    fig = render_top_risky_measures_with_influence(ranked_measures, tolerance=tolerance, top_n=10)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # Gauge de score promedio vs tolerancia
                    fig_gauge = render_tolerance_gauge(stats['avg_score'], tolerance)
                    st.plotly_chart(fig_gauge, use_container_width=True)

                st.markdown("---")

                # Issues más frecuentes
                render_top_issues(ranked_measures)

                st.markdown("---")

                # Tabla de medidas
                render_measures_table(ranked_measures)
            else:
                st.warning("⚠️ No se encontraron medidas en el archivo PBIP")

        except Exception as e:
            st.error(f"❌ Error al analizar el archivo: {str(e)}")

        finally:
            # Limpiar archivo temporal si se creó
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    else:
        # Mostrar instrucciones si no hay archivo
        st.info("""
        👆 **¡Listo para analizar!** Proporciona la ruta al archivo .pbip para comenzar.

        **Recuerda:** Puedes pegar la ruta al archivo `.pbip` con o sin comillas.
        La aplicación se encargará de buscar la carpeta `.SemanticModel` automáticamente.
        """)

        # Ejemplo visual de cómo funciona
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                    border-radius: 12px; padding: 20px; margin-top: 20px; border-left: 5px solid #0066cc;">
            <h4 style="color: #0066cc; margin-top: 0;">💡 Ejemplo de uso</h4>
            <ol style="color: #495057;">
                <li><strong>Copia la ruta de tu archivo PBIP</strong> desde el explorador de Windows</li>
                <li><strong>Pégala en el campo de arriba</strong> (con o sin comillas)</li>
                <li><strong>La aplicación procesará automáticamente</strong> todas las medidas DAX</li>
                <li><strong>Revisa los resultados</strong> y exporta el análisis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
