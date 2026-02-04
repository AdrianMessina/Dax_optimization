# Quick Start - DAX Optimizer v1.1

## Inicio rápido en 3 pasos

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

**Opción A - Windows (Recomendado):**
```bash
run_dax_optimizer.bat
```

**Opción B - Línea de comandos:**
```bash
streamlit run streamlit_app/app.py
```

**Opción C - Crear acceso directo:**
```powershell
powershell -ExecutionPolicy Bypass -File create-shortcut.ps1
```

### 3. Analizar tu archivo PBIP

1. Abre tu navegador (se abre automáticamente en http://localhost:8501)
2. Haz clic en "Browse files" y selecciona tu archivo .pbip
3. Espera a que se complete el análisis
4. Revisa el dashboard con estadísticas
5. Explora la tabla de medidas rankeadas
6. Expande cualquier medida para ver detalles

---

## Ejemplo de uso

### Preparar tu archivo PBIP

Para obtener un archivo PBIP de Power BI Desktop:

1. Abre tu informe en Power BI Desktop
2. Ve a **Archivo > Guardar como**
3. Selecciona la ubicación y guarda el archivo
4. El archivo .pbip se creará (es un archivo ZIP)

### Interpretar los resultados

#### Dashboard de resumen
- **Total de medidas**: Cantidad total analizada
- **Críticas**: Medidas con problemas severos (score 0-40)
- **Alta prioridad**: Medidas con varios warnings (score 41-60)
- **Problemas críticos**: Suma de todos los issues críticos

#### Tabla de medidas
Cada fila muestra:
- **Nombre**: Nombre de la medida
- **Score**: Puntuación de 0-100 (menor = más problemas)
- **Impacto**: 🔴 Crítico / 🟠 Alto / 🟡 Medio / 🟢 Bajo
- **🔴**: Cantidad de problemas críticos
- **⚠️**: Cantidad de warnings
- **Complejidad**: Score de complejidad del código

#### Vista detallada
Al expandir una medida verás:
- **Código DAX**: El código completo de la medida
- **Análisis**: Problemas detectados con explicaciones
- **Sugerencias**: Código mejorado con ejemplos
- **Métricas**: Estadísticas de performance

---

## Problemas comunes

### "ModuleNotFoundError: No module named 'streamlit'"
**Solución**: Instala las dependencias
```bash
pip install -r requirements.txt
```

### "Error al extraer medidas del PBIP"
**Posibles causas**:
- El archivo no es un PBIP válido
- El archivo está corrupto
- El formato no es compatible

**Solución**: Verifica que el archivo:
- Tenga extensión .pbip
- Se haya exportado correctamente desde Power BI Desktop
- No esté dañado

### "No se encontraron medidas"
**Posibles causas**:
- El modelo no tiene medidas DAX
- Las medidas están en un formato no reconocido

**Solución**:
- Verifica que tu modelo tenga medidas definidas
- Asegúrate de usar Power BI Desktop actualizado

---

## Tips de uso

### Priorizar el trabajo
1. Ordena por score (menor primero)
2. Enfócate en medidas 🔴 Críticas primero
3. Expande y lee el análisis detallado
4. Implementa las sugerencias de optimización

### Filtrar medidas
- Usa el filtro de prioridad para ver solo críticas/altas
- Usa la búsqueda para encontrar medidas específicas
- Cambia el orden según tus necesidades

### Interpretar sugerencias
- **Impacto HIGH** 🔥: Implementa PRIMERO
- **Impacto MEDIUM** 💡: Implementa cuando sea posible
- **Impacto LOW** ℹ️: Mejoras opcionales

### Exportar resultados
Toma screenshots del dashboard y de las medidas críticas para:
- Documentar el estado actual
- Justificar tiempo de refactorización
- Hacer seguimiento de mejoras

---

## Próximos pasos

Después de analizar tu archivo:

1. **Prioriza**: Enfócate en medidas con score < 40
2. **Refactoriza**: Implementa las sugerencias de optimización
3. **Prueba**: Verifica que los resultados sean correctos
4. **Re-analiza**: Vuelve a cargar el PBIP para ver mejoras
5. **Mide**: Compara performance antes/después con DAX Studio

---

## Recursos adicionales

### Documentación
- [README.md](README.md) - Documentación completa
- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios

### Enlaces útiles
- [SQLBI - DAX Patterns](https://www.sqlbi.com/patterns/)
- [DAX Guide](https://dax.guide/)
- [DAX Studio](https://daxstudio.org/) - Para medir performance real

### Soporte
Si encuentras problemas:
1. Revisa los logs en la consola
2. Verifica que el archivo PBIP sea válido
3. Asegúrate de tener la última versión de las dependencias
