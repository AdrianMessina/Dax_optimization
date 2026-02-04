# 🚀 Instalación Rápida - DAX Optimizer v1.1.2

## 📦 Nueva Dependencia

Esta versión incluye una nueva dependencia para la funcionalidad de exportación a Excel:

```bash
openpyxl==3.1.2
```

## 🔧 Instalación

### Opción 1: Instalar todas las dependencias

```bash
pip install -r requirements.txt
```

### Opción 2: Instalar solo la nueva dependencia

```bash
pip install openpyxl==3.1.2
```

## ✅ Verificar instalación

Para verificar que la instalación fue exitosa, ejecuta:

```bash
python -c "import openpyxl; print('✅ openpyxl instalado correctamente - Versión:', openpyxl.__version__)"
```

## 🎯 Ejecutar la aplicación

### Método 1: Usando el archivo batch (Windows)

```bash
run_dax_optimizer.bat
```

### Método 2: Comando directo

```bash
streamlit run streamlit_app/app.py
```

### Método 3: Desde PowerShell

```powershell
cd "C:\Users\SE46958\1 - Claude - Proyecto viz\Dax optimization\dax-optimizer-streamlit-v1.1"
streamlit run streamlit_app/app.py
```

## 📋 Lista completa de dependencias

```
streamlit==1.31.0
plotly==5.18.0
pandas==2.1.4
pyyaml==6.0.1
openpyxl==3.1.2  ← NUEVA
```

## 🐛 Solución de problemas

### Error: "No module named 'openpyxl'"

**Solución:**
```bash
pip install openpyxl
```

### Error: "pip not found"

**Solución:**
```bash
python -m pip install openpyxl
```

### Error de permisos en Windows

**Solución:**
```bash
pip install --user openpyxl
```

## 📁 Estructura de archivos actualizada

```
dax-optimizer-streamlit-v1.1/
├── streamlit_app/
│   ├── app.py                    ← Actualizado
│   ├── assets/
│   │   └── dax_optimization.ico  ← NUEVO
│   └── __init__.py
├── core/
│   └── (archivos existentes)
├── requirements.txt              ← Actualizado
├── MEJORAS_V1.1.2.md            ← NUEVO
├── RESUMEN_VISUAL_MEJORAS.txt   ← NUEVO
└── INSTALACION_RAPIDA.md        ← Este archivo
```

## 🎨 Características nuevas disponibles

✅ Exportación a CSV
✅ Exportación a Excel con formato
✅ Animaciones de análisis
✅ Diseño mejorado
✅ Ícono oficial

## 📞 Soporte

Si encuentras algún problema durante la instalación o ejecución:

1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de estar en el directorio correcto
3. Verifica que Python 3.8+ esté instalado
4. Revisa el archivo MEJORAS_V1.1.2.md para más detalles

---

**Desarrollado por**: Adrián Javier Messina | Torre Visualización
**Versión**: v1.1.2
**Fecha**: 3 de Febrero 2026
