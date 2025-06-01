#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renombrador Universal de Carpetas
Normaliza nombres eliminando espacios, acentos y caracteres especiales
Versión Universal - Para cualquier tipo de carpetas
Autor: rodrigoangeloni
Fecha: 2025-06-01
"""

import os
import re
import sys
import unicodedata
from pathlib import Path
import time
from datetime import datetime

# Configuración para PyInstaller
def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y para PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def pause_and_exit():
    """Pausa antes de cerrar la ventana"""
    print("\nPresiona Enter para cerrar...")
    try:
        input()
    except:
        time.sleep(3)
    sys.exit()

def clear_screen():
    """Limpia la pantalla"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\n" * 50)

def normalize_folder_name(name, options=None):
    """
    Normaliza el nombre de la carpeta según las opciones especificadas
    """
    if not name or not isinstance(name, str):
        return 'unnamed_folder'
    
    original_name = name
    
    # Opciones por defecto
    if options is None:
        options = {
            'lowercase': True,
            'remove_accents': True,
            'replace_spaces': True,
            'remove_special': True,
            'preserve_numbers': True,
            'preserve_dots': False
        }
    
    # Convertir a minúsculas si está habilitado
    if options.get('lowercase', True):
        name = name.lower()
    
    # Eliminar acentos si está habilitado
    if options.get('remove_accents', True):
        try:
            name = unicodedata.normalize('NFD', name)
            name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
        except:
            pass
    
    # Construir patrón de caracteres permitidos
    allowed_chars = r'a-zA-Z'
    
    if options.get('preserve_numbers', True):
        allowed_chars += r'0-9'
    
    if options.get('preserve_dots', False):
        allowed_chars += r'\.'
    
    # Reemplazar espacios
    if options.get('replace_spaces', True):
        name = re.sub(r'\s+', '_', name)
        allowed_chars += r'_'
    else:
        allowed_chars += r'\s'
    
    # Eliminar caracteres especiales si está habilitado
    if options.get('remove_special', True):
        pattern = f'[^{allowed_chars}]'
        name = re.sub(pattern, '_', name)
    
    # Limpiar múltiples guiones bajos consecutivos
    name = re.sub(r'_+', '_', name)
    
    # Eliminar guiones bajos al inicio y final
    name = name.strip('_')
    
    # Si el nombre queda vacío, usar un nombre por defecto
    if not name:
        name = 'unnamed_folder'
    
    return name

def get_exe_directory():
    """Obtiene el directorio donde está el ejecutable o script"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def show_welcome_screen():
    """Muestra la pantalla de bienvenida con información del programa"""
    clear_screen()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "RENOMBRADOR UNIVERSAL DE CARPETAS v2.0" + " " * 19 + "║")
    print("║" + " " * 30 + "by rodrigoangeloni" + " " * 30 + "║")
    print("╠" + "═" * 78 + "╣")
    print("║                                                                              ║")
    print("║  🎯 ¿QUÉ HACE ESTE PROGRAMA?                                                 ║")
    print("║      Este programa normaliza los nombres de carpetas eliminando:            ║")
    print("║      • Espacios (los convierte en guiones bajos)                            ║")
    print("║      • Acentos y caracteres especiales (ñ→n, á→a, etc.)                    ║")
    print("║      • Caracteres problemáticos para sistemas                               ║")
    print("║                                                                              ║")
    print("║  📁 EJEMPLOS DE TRANSFORMACIÓN:                                             ║")
    print("║      'Mi Carpeta Especial ñáéíóú' → 'mi_carpeta_especial_naeio'           ║")
    print("║      'Fotos Vacaciones (2024)'    → 'fotos_vacaciones_2024'               ║")
    print("║      'Música - Rock & Roll'       → 'musica_rock_roll'                     ║")
    print("║                                                                              ║")
    print("║  ⚡ CARACTERÍSTICAS:                                                         ║")
    print("║      • Vista previa antes de hacer cambios                                  ║")
    print("║      • Procesamiento por lotes de todas las carpetas                        ║")
    print("║      • Opciones personalizables                                             ║")
    print("║      • Seguro: no modifica archivos, solo nombres de carpetas               ║")
    print("║                                                                              ║")
    print("║  📂 DIRECTORIO DE TRABAJO:                                                  ║")
    print(f"║      {get_exe_directory():<68} ║")
    print("║                                                                              ║")
    print("╚" + "═" * 78 + "╝")
    print("\n🔥 ¡IMPORTANTE! Siempre haz una copia de seguridad antes de usar el programa")
    print("\nPresiona Enter para continuar...")
    try:
        input()
    except:
        time.sleep(3)

def show_options_menu():
    """Muestra el menú de opciones de normalización"""
    options = {
        'lowercase': True,
        'remove_accents': True,
        'replace_spaces': True,
        'remove_special': True,
        'preserve_numbers': True,
        'preserve_dots': False
    }
    
    while True:
        clear_screen()
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "OPCIONES DE NORMALIZACIÓN" + " " * 26 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║                                                                              ║")
        
        status_map = {True: "✅ ACTIVADO ", False: "❌ DESACTIVADO"}
        
        print(f"║  1. Convertir a minúsculas        {status_map[options['lowercase']]:<25} ║")
        print(f"║  2. Eliminar acentos              {status_map[options['remove_accents']]:<25} ║")
        print(f"║  3. Reemplazar espacios por _     {status_map[options['replace_spaces']]:<25} ║")
        print(f"║  4. Eliminar caracteres especiales {status_map[options['remove_special']]:<25} ║")
        print(f"║  5. Preservar números             {status_map[options['preserve_numbers']]:<25} ║")
        print(f"║  6. Preservar puntos              {status_map[options['preserve_dots']]:<25} ║")
        print("║                                                                              ║")
        print("║  7. 🔍 Ver ejemplo con configuración actual                                  ║")
        print("║  8. ✅ Continuar con estas opciones                                          ║")
        print("║  9. 🔙 Volver al menú principal                                              ║")
        print("║                                                                              ║")
        print("╚" + "═" * 78 + "╝")
        
        choice = input("\nSelecciona una opción (1-9): ").strip()
        
        if choice == '1':
            options['lowercase'] = not options['lowercase']
        elif choice == '2':
            options['remove_accents'] = not options['remove_accents']
        elif choice == '3':
            options['replace_spaces'] = not options['replace_spaces']
        elif choice == '4':
            options['remove_special'] = not options['remove_special']
        elif choice == '5':
            options['preserve_numbers'] = not options['preserve_numbers']
        elif choice == '6':
            options['preserve_dots'] = not options['preserve_dots']
        elif choice == '7':
            show_example_transformation(options)
        elif choice == '8':
            return options
        elif choice == '9':
            return None
        else:
            print("❌ Opción no válida. Intenta de nuevo.")
            time.sleep(1)

def show_example_transformation(options):
    """Muestra ejemplos de transformación con las opciones actuales"""
    clear_screen()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "EJEMPLOS DE TRANSFORMACIÓN" + " " * 26 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    examples = [
        "Mi Carpeta Especial ñáéíóú",
        "Fotos Vacaciones (2024)",
        "Música - Rock & Roll",
        "DOCUMENTOS IMPORTANTES!!!",
        "Nueva Carpeta 1.5",
        "Proyecto Final - Versión 2.0"
    ]
    
    for i, example in enumerate(examples, 1):
        transformed = normalize_folder_name(example, options)
        print(f"{i}. '{example}'")
        print(f"   → '{transformed}'")
        print()
    
    print("Presiona Enter para volver...")
    try:
        input()
    except:
        time.sleep(2)

def rename_folders(directory_path, options=None):
    """Renombra todas las carpetas en el directorio especificado"""
    try:
        base_path = Path(directory_path).resolve()
        
        if not base_path.exists():
            print(f"❌ ERROR: El directorio no existe.")
            print(f"Ruta: {directory_path}")
            return False
        
        if not base_path.is_dir():
            print(f"❌ ERROR: La ruta no es un directorio.")
            return False
        
        print(f"📂 Procesando directorio:")
        print(f"   {base_path}")
        print("═" * 80)
        
        try:
            folders = [item for item in base_path.iterdir() if item.is_dir()]
        except PermissionError:
            print("❌ ERROR: Sin permisos para acceder al directorio.")
            return False
        except Exception as e:
            print(f"❌ ERROR al listar carpetas: {e}")
            return False
        
        if not folders:
            print("ℹ️  INFO: No se encontraron carpetas para renombrar.")
            return True
        
        print(f"📁 Se encontraron {len(folders)} carpetas.\n")
        
        renamed_count = 0
        skipped_count = 0
        error_count = 0
        
        for i, folder in enumerate(folders, 1):
            try:
                original_name = folder.name
                new_name = normalize_folder_name(original_name, options)
                
                print(f"[{i:2d}/{len(folders)}] ", end="", flush=True)
                
                if original_name == new_name:
                    print(f"✅ Sin cambios: '{original_name}'")
                    skipped_count += 1
                    continue
                
                new_path = folder.parent / new_name
                
                if new_path.exists():
                    print(f"⚠️  CONFLICTO: '{original_name}' → '{new_name}' (ya existe)")
                    error_count += 1
                    continue
                
                folder.rename(new_path)
                print(f"🔄 RENOMBRADO: '{original_name}' → '{new_name}'")
                renamed_count += 1
                
            except PermissionError:
                print(f"❌ ERROR: Sin permisos para renombrar '{folder.name}'")
                error_count += 1
            except OSError as e:
                print(f"❌ ERROR renombrando '{folder.name}': {e}")
                error_count += 1
            except Exception as e:
                print(f"❌ ERROR inesperado con '{folder.name}': {e}")
                error_count += 1
        
        print("\n" + "═" * 80)
        print("📊 RESUMEN:")
        print(f"   ✅ Carpetas renombradas: {renamed_count}")
        print(f"   ➡️  Carpetas sin cambios: {skipped_count}")
        print(f"   ❌ Errores/conflictos: {error_count}")
        print(f"   📁 Total procesadas: {len(folders)}")
        
        if renamed_count > 0:
            print(f"\n🎉 ¡Renombrado completado exitosamente!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR general: {e}")
        return False

def preview_changes(directory_path, options=None):
    """Muestra una vista previa de los cambios que se realizarían"""
    try:
        base_path = Path(directory_path).resolve()
        
        if not base_path.exists() or not base_path.is_dir():
            print(f"❌ ERROR: Directorio no válido.")
            return False
        
        print(f"🔍 Vista previa de cambios en:")
        print(f"   {base_path}")
        print("═" * 80)
        
        try:
            folders = [item for item in base_path.iterdir() if item.is_dir()]
        except PermissionError:
            print("❌ ERROR: Sin permisos para acceder al directorio.")
            return False
        except Exception as e:
            print(f"❌ ERROR al listar carpetas: {e}")
            return False
        
        if not folders:
            print("ℹ️  INFO: No se encontraron carpetas.")
            return True
        
        changes_count = 0
        conflicts_count = 0
        
        print("📋 CAMBIOS PROPUESTOS:\n")
        
        for i, folder in enumerate(folders, 1):
            try:
                original_name = folder.name
                new_name = normalize_folder_name(original_name, options)
                
                print(f"[{i:2d}] ", end="")
                
                if original_name != new_name:
                    new_path = folder.parent / new_name
                    if new_path.exists():
                        print(f"⚠️  '{original_name}' → '{new_name}' (CONFLICTO - ya existe)")
                        conflicts_count += 1
                    else:
                        print(f"🔄 '{original_name}' → '{new_name}'")
                        changes_count += 1
                else:
                    print(f"✅ '{original_name}' (sin cambios)")
                    
            except Exception as e:
                print(f"[{i:2d}] ❌ ERROR procesando carpeta: {e}")
        
        print("\n" + "═" * 80)
        print(f"📊 Se realizarían {changes_count} cambios de {len(folders)} carpetas.")
        if conflicts_count > 0:
            print(f"⚠️  Advertencia: {conflicts_count} conflictos detectados.")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Función principal con menú interactivo moderno"""
    try:
        # Configurar la consola para Windows
        if os.name == 'nt':
            try:
                os.system('title Renombrador Universal de Carpetas v2.0')
                os.system('mode con: cols=85 lines=40')
                os.system('chcp 65001 >nul 2>&1')
            except:
                pass
        
        # Mostrar pantalla de bienvenida
        show_welcome_screen()
        
        # Obtener el directorio de trabajo
        exe_dir = get_exe_directory()
        current_options = None
        
        while True:
            clear_screen()
            print("╔" + "═" * 78 + "╗")
            print("║" + " " * 20 + "RENOMBRADOR UNIVERSAL DE CARPETAS" + " " * 23 + "║")
            print("║" + " " * 35 + "MENÚ PRINCIPAL" + " " * 30 + "║")
            print("╠" + "═" * 78 + "╣")
            print("║                                                                              ║")
            print("║  📂 Directorio de trabajo:                                                   ║")
            print(f"║     {exe_dir:<68} ║")
            print("║                                                                              ║")
            print("║  🎯 OPCIONES DISPONIBLES:                                                    ║")
            print("║                                                                              ║")
            print("║     1. ⚙️  Configurar opciones de normalización                              ║")
            print("║     2. 🔍 Vista previa de cambios                                            ║")
            print("║     3. 🚀 Ejecutar renombrado                                                ║")
            print("║     4. ❓ Mostrar ayuda                                                       ║")
            print("║     5. 🚪 Salir                                                              ║")
            print("║                                                                              ║")
            
            if current_options:
                print("║  ✅ Opciones configuradas: SÍ                                               ║")
            else:
                print("║  ⚙️  Opciones configuradas: Usando valores por defecto                      ║")
            
            print("║                                                                              ║")
            print("╚" + "═" * 78 + "╝")
            
            choice = input("\n🎯 Selecciona una opción (1-5): ").strip()
            
            if choice == '1':
                new_options = show_options_menu()
                if new_options is not None:
                    current_options = new_options
                    print("✅ Opciones configuradas correctamente.")
                    time.sleep(1)
                    
            elif choice == '2':
                clear_screen()
                print("╔" + "═" * 78 + "╗")
                print("║" + " " * 30 + "VISTA PREVIA" + " " * 33 + "║")
                print("╚" + "═" * 78 + "╝")
                print()
                if preview_changes(exe_dir, current_options):
                    print("\n🔍 Vista previa completada.")
                else:
                    print("\n❌ Error en la vista previa.")
                input("\nPresiona Enter para continuar...")
                
            elif choice == '3':
                clear_screen()
                print("╔" + "═" * 78 + "╗")
                print("║" + " " * 30 + "EJECUTAR RENOMBRADO" + " " * 27 + "║")
                print("╚" + "═" * 78 + "╝")
                print()
                print("⚠️  ATENCIÓN: Esta operación renombrará las carpetas permanentemente.")
                print("🔒 Asegúrate de tener una copia de seguridad si es necesario.")
                print()
                confirm = input("🤔 ¿Estás seguro de que quieres continuar? (S/n): ").strip().lower()
                
                if confirm in ['s', 'si', 'y', 'yes', '']:
                    print("\n🚀 Iniciando renombrado...\n")
                    if rename_folders(exe_dir, current_options):
                        print("\n✅ Proceso completado.")
                    else:
                        print("\n❌ El proceso terminó con errores.")
                else:
                    print("\n🚫 Operación cancelada.")
                
                input("\nPresiona Enter para continuar...")
                
            elif choice == '4':
                show_help()
                
            elif choice == '5':
                clear_screen()
                print("╔" + "═" * 78 + "╗")
                print("║" + " " * 25 + "¡GRACIAS POR USAR EL PROGRAMA!" + " " * 22 + "║")
                print("║" + " " * 20 + "Que tengas un excelente día organizando" + " " * 19 + "║")
                print("║" + " " * 30 + "tus carpetas! 📁✨" + " " * 29 + "║")
                print("╚" + "═" * 78 + "╝")
                time.sleep(2)
                break
                
            else:
                print("❌ Opción no válida. Por favor, selecciona 1, 2, 3, 4 o 5.")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\n🚫 Operación cancelada por el usuario.")
        pause_and_exit()
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("El programa se cerrará en 5 segundos...")
        time.sleep(5)
        pause_and_exit()

def show_help():
    """Muestra la pantalla de ayuda"""
    clear_screen()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 32 + "AYUDA Y GUÍA" + " " * 33 + "║")
    print("╠" + "═" * 78 + "╣")
    print("║                                                                              ║")
    print("║  🎯 PROPÓSITO:                                                               ║")
    print("║      Este programa normaliza nombres de carpetas para hacerlos más          ║")
    print("║      compatibles con diferentes sistemas y servidores.                      ║")
    print("║                                                                              ║")
    print("║  📋 PASOS RECOMENDADOS:                                                      ║")
    print("║      1. Configura las opciones según tus necesidades                        ║")
    print("║      2. Usa la vista previa para ver qué cambios se harán                   ║")
    print("║      3. Ejecuta el renombrado solo si estás satisfecho                      ║")
    print("║                                                                              ║")
    print("║  ⚙️  OPCIONES PRINCIPALES:                                                   ║")
    print("║      • Minúsculas: Convierte TODO a minúsculas                              ║")
    print("║      • Eliminar acentos: ñ→n, á→a, é→e, etc.                               ║")
    print("║      • Reemplazar espacios: Los convierte en guiones bajos (_)              ║")
    print("║      • Eliminar especiales: Quita símbolos como @#$%&*()                   ║")
    print("║      • Preservar números: Mantiene los números (0-9)                        ║")
    print("║      • Preservar puntos: Mantiene los puntos (.)                            ║")
    print("║                                                                              ║")
    print("║  🛡️  SEGURIDAD:                                                              ║")
    print("║      • Solo renombra carpetas, NO toca archivos                             ║")
    print("║      • No borra ni modifica contenido                                       ║")
    print("║      • Detecta conflictos antes de hacer cambios                            ║")
    print("║                                                                              ║")
    print("║  💡 CONSEJO: Siempre haz una copia de seguridad antes de usar!              ║")
    print("║                                                                              ║")
    print("╚" + "═" * 78 + "╝")
    input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    main()
