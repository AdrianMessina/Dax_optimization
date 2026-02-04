#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que todos los imports funcionan
"""

import sys
from pathlib import Path

# Agregar path del proyecto
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("VERIFICACION DE IMPORTS - DAX OPTIMIZER")
print("=" * 60)

# Test 1: Dependencias basicas
print("\n1. Verificando dependencias basicas...")
try:
    import streamlit
    print("   [OK] streamlit")
except ImportError as e:
    print(f"   [ERROR] streamlit: {e}")
    sys.exit(1)

try:
    import plotly
    print("   [OK] plotly")
except ImportError as e:
    print(f"   [ERROR] plotly: {e}")
    sys.exit(1)

try:
    import pandas
    print("   [OK] pandas")
except ImportError as e:
    print(f"   [ERROR] pandas: {e}")
    sys.exit(1)

try:
    import yaml
    print("   [OK] pyyaml")
except ImportError as e:
    print(f"   [ERROR] pyyaml: {e}")
    sys.exit(1)

# Test 2: Dependencias opcionales
print("\n2. Verificando dependencias opcionales...")
try:
    from streamlit_extras.metric_cards import style_metric_cards
    print("   [OK] streamlit-extras")
    EXTRAS_OK = True
except ImportError:
    print("   [WARNING] streamlit-extras (opcional - no instalado)")
    EXTRAS_OK = False

try:
    from streamlit_lottie import st_lottie
    print("   [OK] streamlit-lottie")
    LOTTIE_OK = True
except ImportError:
    print("   [WARNING] streamlit-lottie (opcional - no instalado)")
    LOTTIE_OK = False

# Test 3: Modulos del core
print("\n3. Verificando modulos del core...")
try:
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
    print("   [OK] Todos los modulos del core")
except ImportError as e:
    print(f"   [ERROR] Error en modulos del core: {e}")
    sys.exit(1)

# Resumen
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print("\n[OK] DEPENDENCIAS BASICAS: OK")
print(f"[{'OK' if EXTRAS_OK else 'WARNING'}] STREAMLIT-EXTRAS: {'Instalado' if EXTRAS_OK else 'No instalado (usando fallback)'}")
print(f"[{'OK' if LOTTIE_OK else 'WARNING'}] STREAMLIT-LOTTIE: {'Instalado' if LOTTIE_OK else 'No instalado (usando fallback)'}")
print("[OK] MODULOS DEL CORE: OK")

print("\n" + "=" * 60)
if EXTRAS_OK and LOTTIE_OK:
    print("RESULTADO: [OK] TODAS LAS FUNCIONALIDADES DISPONIBLES")
    print("           La app funcionara con todas las mejoras visuales.")
else:
    print("RESULTADO: [WARNING] FUNCIONALIDAD BASICA DISPONIBLE")
    print("           La app funcionara correctamente, pero sin algunas")
    print("           mejoras visuales opcionales.")
    print("\n           Para habilitar todas las mejoras visuales, ejecuta:")
    print("           pip install streamlit-extras streamlit-lottie")
print("=" * 60)

print("\n[OK] La aplicacion esta lista para ejecutarse con:")
print("  streamlit run streamlit_app/app.py")
print("\nSi ves errores de imports, la app funcionara de todas formas")
print("usando las versiones de fallback (sin mejoras visuales extras).")
