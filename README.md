# 📁 Renombrador Universal de Carpetas v2.0

> **🎉 Versión 2.0 - GUI Moderna + Terminal**  
> 4 versiones compiladas: Terminal y GUI para Windows/Linux usando WSL

Una herramienta moderna y multiplataforma para normalizar nombres de carpetas, eliminando espacios, acentos y caracteres especiales. Disponible con interfaz gráfica moderna y versión terminal. Perfecta para organizar carpetas de skins de Assetto Corsa y cualquier otro tipo de archivos.

## 🆕 Nuevo en v2.0
- **🖼️ Interfaz Gráfica Moderna**: GUI completa con tkinter
- **📋 Previsualización en Tiempo Real**: Ve los cambios antes de aplicarlos
- **📑 Sistema de Pestañas**: Vista previa y registro de actividad
- **⚙️ Configuración Visual**: Checkboxes para todas las opciones
- **🎯 Selección de Directorio**: Navegador de carpetas integrado
- **📈 Barra de Progreso**: Seguimiento visual del proceso
- **❓ Sistema de Ayuda**: Ejemplos interactivos y documentación
- **🧵 Procesamiento Asíncrono**: Interfaz no bloqueante durante operaciones

## 🎯 ¿Para qué sirve?

Este programa es perfecto cuando necesitas:
- **Normalizar carpetas** para compatibilidad con servidores
- **Eliminar espacios** y caracteres problemáticos  
- **Quitar acentos** (ñ→n, á→a, é→e, etc.)
- **Procesar múltiples carpetas** de una vez
- **Ver una vista previa** antes de hacer cambios
- **Mantener organización** en colecciones de mods

## ✨ Características Principales

### 🖥️ Doble Interfaz
- **GUI Moderna**: Interfaz gráfica intuitiva con tkinter
- **Terminal Clásica**: Versión línea de comandos para automatización
- Misma funcionalidad en ambas versiones
- Configuraciones sincronizadas entre versiones

### ⚙️ Opciones Personalizables
- **Convertir a minúsculas**: TODO → todo
- **Eliminar acentos**: café → cafe
- **Reemplazar espacios**: Mi Carpeta → mi_carpeta
- **Eliminar caracteres especiales**: @#$%&*() → _
- **Preservar números**: 2024 → 2024
- **Preservar puntos**: archivo.txt → archivo.txt

### 🛡️ Seguro y Confiable
- Vista previa antes de ejecutar cambios
- Detección de conflictos
- Solo renombra carpetas (no toca archivos)
- Manejo robusto de errores
- Registro detallado de todas las operaciones

## 🎮 Uso del Programa

### Opción 1: Ejecutables Precompilados (Recomendado)

Descarga la versión que necesites:

#### Windows
- **GUI**: `renombrador-gui-windows.exe` - Interfaz gráfica moderna
- **Terminal**: `renombrador-terminal-windows.exe` - Línea de comandos

#### Linux  
- **GUI**: `renombrador-gui-linux` - Interfaz gráfica moderna
- **Terminal**: `renombrador-terminal-linux` - Línea de comandos

**Uso GUI**:
1. Ejecuta el archivo GUI correspondiente
2. Selecciona la carpeta usando el botón "Examinar"
3. Configura las opciones con los checkboxes
4. Revisa la previsualización en la pestaña "Vista Previa"
5. Haz clic en "Renombrar Carpetas" para aplicar cambios

**Uso Terminal**:
1. Copia el ejecutable terminal a la carpeta que contiene las subcarpetas
2. Ejecuta el programa desde terminal o doble clic
3. Sigue las instrucciones en pantalla

### Opción 2: Ejecutar desde Python

**GUI Version**:
```bash
# Asegúrate de tener Python 3.7+ y tkinter instalado
python rename_folders_gui.py
```

**Terminal Version**:
```bash
# Asegúrate de tener Python 3.7+ instalado
python rename_folders.py
```

### 🎯 Flujo de Uso

**Interfaz Gráfica (GUI)**:
1. **Selección**: Elige la carpeta con el navegador
2. **Configuración**: Marca/desmarca opciones con checkboxes
3. **Vista previa**: Revisa cambios en la pestaña "Vista Previa"
4. **Ejecución**: Haz clic en "Renombrar Carpetas"
5. **Seguimiento**: Observa el progreso y logs en tiempo real

**Terminal**:
1. **Vista previa**: Revisa qué cambios se realizarían
2. **Confirmación**: Decide si proceder con los cambios
3. **Ejecución**: El programa renombra las carpetas automáticamente
4. **Resumen**: Muestra estadísticas de los cambios realizados

## 📋 Ejemplos de Transformación

| Nombre Original | Resultado |
|----------------|-----------|
| `Mi Carpeta Especial ñáéíóú` | `mi_carpeta_especial_naeio` |
| `Fotos Vacaciones (2024)` | `fotos_vacaciones_2024` |
| `Música - Rock & Roll` | `musica_rock_roll` |
| `DOCUMENTOS IMPORTANTES!!!` | `documentos_importantes` |
| `Skins Ferrari F40 (Assetto Corsa)` | `skins_ferrari_f40_assetto_corsa` |

## 🚀 Compilación Universal (4 Versiones desde Windows)

Este proyecto está **optimizado para Windows con WSL** para generar automáticamente **4 ejecutables** en una sola compilación:
- Terminal Windows + GUI Windows
- Terminal Linux + GUI Linux

### 📋 Prerrequisitos (Solo Windows)

1. **Windows 10/11** 
2. **WSL instalado** (se instala automáticamente si no existe):
   ```powershell
   wsl --install
   ```
3. **Python 3.x** instalado en Windows

### 🚀 Compilar las 4 Versiones

El sistema automáticamente:
- ✅ **Compila 2 versiones Windows** (Terminal + GUI) usando Python local
- ✅ **Compila 2 versiones Linux** (Terminal + GUI) usando WSL automáticamente 
- ✅ **Instala dependencias** automáticamente (incluso en entornos gestionados)
- ✅ **Maneja errores** de instalación de PyInstaller en WSL
- ✅ **Instala tkinter** para soporte GUI en Linux

**Ejecutar compilación universal**:
```bash
python compilar_universal.py
```

### 📦 Archivos Resultantes

Después de la compilación encontrarás en `/dist`:
- `renombrador-terminal-windows.exe` (6.7 MB)
- `renombrador-gui-windows.exe` (9.6 MB) 
- `renombrador-terminal-linux` (6.8 MB)
- `renombrador-gui-linux` (6.8 MB)
- `README.txt` (Documentación completa)

### 📦 Resultado de la Compilación

```
dist/
├── renombrador-universal-windows.exe  (~6.7 MB) ✅
├── renombrador-universal-linux        (~6.8 MB) ✅
└── README.txt                         (instrucciones de uso)
```

### 🔧 Configuración Automática

El compilador se encarga automáticamente de:
- **Detectar WSL** y sugerir instalación si no existe
- **Instalar PyInstaller** en entornos Python gestionados externamente
- **Manejar permisos** de Linux automáticamente
- **Generar ejecutables** para ambas plataformas
- **Crear documentación** de distribución

### 🐛 Solución de Problemas

**WSL no disponible:**
```powershell
# Ejecutar como Administrador:
wsl --install
# Reiniciar Windows y ejecutar de nuevo
```

**Error de permisos PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Python no encontrado:**
- Instala Python desde [python.org](https://python.org)
- Reinicia la terminal y ejecuta de nuevo

## 📁 Estructura de Salida

```
dist/
├── windows/
│   └── renombrador-universal-windows.exe
├── linux/
│   └── renombrador-universal-linux
└── release/
    ├── renombrador-universal-windows.exe
    ├── renombrador-universal-linux
    └── README.txt
```

## ⚙️ Características del Compilador Universal

- **Detección automática** de dependencias
- **Instalación automática** de PyInstaller si no está presente
- **Configuración automática** de WSL si es necesario
- **Compilación inteligente** para ambas plataformas
- **Manejo robusto de errores** con mensajes claros
- **Progreso visual** durante la compilación

## 🔧 Configuración Automática de WSL

El compilador universal se encarga automáticamente de:

### 1. Verificar WSL
- Detecta si WSL está instalado
- Sugiere instalación si no está disponible

### 2. Configurar Ubuntu
- Instala Ubuntu automáticamente si no existe
- Configura Python3 y pip
- Instala PyInstaller en el entorno WSL

### 3. Sincronización
- Copia archivos fuente al entorno WSL
- Ejecuta compilación Linux
- Recupera ejecutables compilados

## 🐛 Solución de Problemas

### Error: "WSL no está disponible"
- Ejecuta como Admin: `wsl --install`
- Reinicia el sistema
- Ejecuta el compilador de nuevo

### Error: "Python no encontrado"
- El compilador instalará Python automáticamente en WSL
- En Windows, instala Python desde python.org

### Error de permisos
- Ejecuta PowerShell como Administrador
- O usa: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 📊 Verificación Automática

El compilador universal incluye:
- **Verificación de ejecutables** después de compilar
- **Tests automáticos** de funcionalidad básica
- **Reporte de tamaños** de archivos generados
- **Estadísticas de compilación**

## 🎁 Distribución Automática

El proceso genera automáticamente:
- Ejecutables listos para usar
- Documentación de distribución
- Archivos organizados por plataforma
- Package completo en `dist/release/`

## 📝 Logs Automáticos

Todos los procesos generan logs detallados:
- `compilacion_windows.log` - Log de compilación Windows
- `compilacion_linux.log` - Log de compilación Linux (WSL)
- `compilacion_universal.log` - Log del proceso completo

## 🔄 Limpieza Automática

El compilador incluye opciones de limpieza:
- Limpieza de archivos temporales
- Eliminación de builds anteriores
- Reset completo del entorno de compilación

## 📞 Soporte y Contribución

### 🐛 Reportar Problemas

Si encuentras problemas:

1. Revisa los logs automáticos generados
2. Ejecuta el compilador con opción de debug
3. Verifica que tienes permisos de administrador
4. Consulta la sección de solución de problemas

### 🤝 Contribuir

Este es un proyecto open source. Las contribuciones son bienvenidas:

- **Reporta bugs** usando GitHub Issues
- **Propón mejoras** y nuevas características
- **Envía pull requests** con fixes o mejoras
- **Mejora la documentación**

### 👨‍💻 Autor

**rodrigoangeloni** - Desarrollador principal

### 📄 Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

### 🌟 Agradecimientos

- Comunidad de Assetto Corsa por la inspiración
- PyInstaller por hacer posible la compilación multiplataforma
- Microsoft por WSL que permite desarrollo Linux en Windows

---

**¿Te ha sido útil este proyecto? ⭐ Dale una estrella en GitHub!**

## 🏗️ Estructura Limpia del Proyecto

```
rename_ac_skins/
├── rename_folders.py           # 🎯 Programa principal
├── compilar_universal.py       # 🚀 Compilador dual inteligente
├── compilar_simple.bat         # ⚡ Launcher fácil (doble clic)
├── compilar_simple.ps1         # 🔧 Launcher PowerShell
├── README.md                   # 📖 Documentación completa
├── LICENSE                     # 📄 Licencia MIT
├── .gitignore                  # 🔒 Control de versiones
└── dist/                       # 📦 Ejecutables generados
    ├── renombrador-universal-windows.exe
    ├── renombrador-universal-linux
    └── README.txt
```

**✨ Solo 7 archivos esenciales** - Sin redundancias ni configuraciones complejas

## 💡 Casos de Uso Comunes

### Para Gamers de Assetto Corsa:
- Normalizar nombres de carpetas de skins descargadas
- Preparar mods para subir a servidores
- Organizar colecciones de coches y tracks

### Para Desarrolladores:
- Limpiar nombres de directorios de proyectos
- Preparar assets para deploy
- Normalizar estructura de archivos

### Para Administradores de Sistema:
- Batch renaming de directorios
- Limpieza masiva de filesystem
- Preparación de archivos para backup

## 🎯 Ventajas de la Versión Simplificada

### ✅ Más Fácil de Usar
- Solo 7 archivos esenciales
- Proceso de compilación unificado
- Configuración automática
- Sin archivos de configuración complejos

### ✅ Más Confiable
- Menos dependencias
- Manejo automático de errores
- Instalación automática de requisitos
- Logs detallados para debug

### ✅ Más Mantenible
- Código consolidado
- Menos archivos que mantener
- Documentación simplificada
- Estructura clara y lógica

### ✅ Listo para GitHub
- Estructura estándar de proyecto
- Archivos mínimos necesarios
- README completo y claro
- Fácil clonado y uso inmediato

## 🚀 Instrucciones de Inicio Rápido

### Para usuarios nuevos:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/rename_ac_skins.git
   cd rename_ac_skins
   ```

2. **Compila los ejecutables**:
   ```batch
   # Windows - doble clic en:
   compilar_simple.bat
   ```

3. **Usa los ejecutables**:
   - Copia `dist/release/renombrador-universal-windows.exe` a tu carpeta de skins
   - Ejecuta y sigue las instrucciones

### Para desarrolladores:

1. **Desarrollo directo**:
   ```bash
   python rename_folders.py
   ```

2. **Compilación avanzada**:
   ```bash
   python compilar_universal.py
   ```

3. **Contribuir**:
   - Fork del proyecto
   - Crear rama de feature
   - Submit pull request

---

## 📈 Historial de Simplificación

**Antes (v0.x)**:
- 11+ archivos de configuración y compilación
- Scripts complejos y redundantes
- Configuración manual requerida
- Estructura confusa

**Ahora (v1.0)**:
- 7 archivos esenciales únicamente
- Un compilador universal inteligente
- Configuración completamente automática
- Estructura clara y lógica

**Resultado**: ✨ **50%+ menos complejidad, 100% más fácil de usar**
