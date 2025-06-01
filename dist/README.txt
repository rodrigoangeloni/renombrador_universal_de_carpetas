# Renombrador Universal v2.0 - Ejecutables Multiplataforma

## 🎯 Contenido Compilado

### Windows:
- **renombrador-terminal-windows.exe** (6.7 MB) - Versión terminal para Windows
- **renombrador-gui-windows.exe** (9.6 MB) - Versión gráfica para Windows

### Linux:
- **renombrador-terminal-linux** (6.8 MB) - Versión terminal para Linux
- **renombrador-gui-linux** (6.8 MB) - Versión gráfica para Linux

## 🚀 Instrucciones de Uso

### Windows Terminal:
1. Copia `renombrador-terminal-windows.exe` a la carpeta con carpetas a renombrar
2. Doble clic para ejecutar
3. Sigue las instrucciones en pantalla

### Windows GUI:
1. Ejecuta `renombrador-gui-windows.exe` desde cualquier ubicación
2. Interfaz gráfica moderna con todas las opciones
3. Selecciona directorio, configura opciones, vista previa y renombra

### Linux Terminal:
1. Copia el ejecutable a la carpeta con carpetas a renombrar
2. Dar permisos: `chmod +x renombrador-terminal-linux`
3. Ejecutar: `./renombrador-terminal-linux`

### Linux GUI:
1. Dar permisos: `chmod +x renombrador-gui-linux`
2. Ejecutar: `./renombrador-gui-linux`
3. Requiere X11/Wayland para la interfaz gráfica

## ✨ Funciones v2.0

### Nuevas Características GUI:
- ✅ **Interfaz gráfica moderna** con tkinter
- ✅ **Selección visual de directorio** con botón examinar
- ✅ **Opciones configurables** con checkboxes intuitivos
- ✅ **Vista previa en tiempo real** con pestañas
- ✅ **Log detallado de resultados** durante el proceso
- ✅ **Ventanas de ayuda** y ejemplos interactivos
- ✅ **Detección automática de conflictos**
- ✅ **Barra de estado** con información en tiempo real

### Características Heredadas v1.0:
- ✅ Elimina espacios, acentos y caracteres especiales
- ✅ Opciones configurables (minúsculas, puntos, números)
- ✅ Vista previa antes de realizar cambios
- ✅ Solo renombra carpetas (preserva archivos)
- ✅ Detección de conflictos
- ✅ Interfaz terminal con colores y emojis

## 📋 Detalles Técnicos

### Compilado con:
- **Python 3.11+** y PyInstaller 6.13.0
- **tkinter** para la interfaz gráfica
- **Sistema dual Windows + WSL** para máxima compatibilidad
- **Compilación automática** desde Windows usando WSL

### Compatibilidad:
- **Windows 10/11** (64-bit)
- **Linux x86_64** (Ubuntu, Debian, etc.)
- **Interfaz GUI** requiere entorno gráfico en Linux

## 🎮 Casos de Uso Perfectos

- **Skins de Assetto Corsa** - Normaliza nombres problemáticos
- **Archivos multimedia** - Organización para servidores
- **Proyectos web** - Nombres compatibles con servidores
- **Desarrollo** - Estructuras de carpetas limpias
- **Migración de sistemas** - Compatibilidad multiplataforma

## 🔧 Opciones de Normalización

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| **Minúsculas** | Convierte todo a minúsculas | `MI CARPETA` → `mi carpeta` |
| **Eliminar acentos** | Quita tildes y caracteres especiales | `ñáéíóú` → `naeio` |
| **Reemplazar espacios** | Convierte espacios en guiones bajos | `mi carpeta` → `mi_carpeta` |
| **Eliminar especiales** | Quita símbolos problemáticos | `carpeta (2024)` → `carpeta_2024` |
| **Preservar números** | Mantiene dígitos 0-9 | `version 2.1` → `version_2_1` |
| **Preservar puntos** | Mantiene puntos en nombres | `version 2.1` → `version_2.1` |

## ⚠️ Seguridad y Precauciones

- 🛡️ **Solo renombra CARPETAS**, no toca archivos
- 🛡️ **No borra ni modifica** contenido de carpetas
- 🛡️ **Detecta conflictos** antes de hacer cambios
- 🛡️ **Vista previa obligatoria** en versión GUI
- 🛡️ **Confirmación explícita** antes de renombrar

## 💡 Consejos de Uso

1. **Siempre haz backup** antes de usar el programa
2. **Usa vista previa** para verificar cambios
3. **Resuelve conflictos** manualmente antes de proceder
4. **Versión GUI** recomendada para usuarios nuevos
5. **Versión terminal** ideal para automatización

## 📊 Estadísticas de Compilación

- **Total de versiones**: 4 ejecutables
- **Plataformas soportadas**: Windows + Linux
- **Interfaces disponibles**: Terminal + GUI
- **Tamaño total**: ~30 MB para todas las versiones
- **Tiempo de compilación**: ~5 minutos en Windows + WSL

---
**Compilado automáticamente el 1 de junio de 2025**  
**Versión 2.0 - Terminal + GUI Multiplataforma**
