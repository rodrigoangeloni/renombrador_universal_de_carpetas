#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renombrador Universal de Carpetas - Versión GUI
Normaliza nombres eliminando espacios, acentos y caracteres especiales
Versión GUI Moderna - Interfaz gráfica intuitiva
Autor: rodrigoangeloni
Fecha: 2025-06-01
"""

import os
import re
import sys
import unicodedata
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from datetime import datetime

class RenombradorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Renombrador Universal de Carpetas v2.0 GUI")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variables de configuración
        self.directory_var = tk.StringVar()
        self.lowercase_var = tk.BooleanVar(value=True)
        self.remove_accents_var = tk.BooleanVar(value=True)
        self.replace_spaces_var = tk.BooleanVar(value=True)
        self.remove_special_var = tk.BooleanVar(value=True)
        self.preserve_numbers_var = tk.BooleanVar(value=True)
        self.preserve_dots_var = tk.BooleanVar(value=False)
        
        # Lista para almacenar vista previa
        self.preview_data = []
        
        self.setup_ui()
        
        # Aplicar tema moderno
        self.apply_modern_theme()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Título principal
        title_label = ttk.Label(main_frame, text="🎯 Renombrador Universal de Carpetas", 
                               font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de selección de directorio
        dir_frame = ttk.LabelFrame(main_frame, text="📂 Directorio de Trabajo", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        dir_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dir_frame, text="Carpeta:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.directory_var, width=60)
        self.dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_btn = ttk.Button(dir_frame, text="Examinar...", command=self.browse_directory)
        self.browse_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.current_dir_btn = ttk.Button(dir_frame, text="Usar Directorio Actual", 
                                        command=self.use_current_directory)
        self.current_dir_btn.grid(row=0, column=3)
        
        # Sección de opciones de configuración
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Opciones de Normalización", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Checkboxes de opciones en dos columnas
        left_options = ttk.Frame(options_frame)
        left_options.grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 20))
        
        right_options = ttk.Frame(options_frame)
        right_options.grid(row=0, column=1, sticky=(tk.W, tk.N))
        
        ttk.Checkbutton(left_options, text="Convertir a minúsculas", 
                       variable=self.lowercase_var, command=self.update_preview).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(left_options, text="Eliminar acentos (ñ→n, á→a)", 
                       variable=self.remove_accents_var, command=self.update_preview).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(left_options, text="Reemplazar espacios con _", 
                       variable=self.replace_spaces_var, command=self.update_preview).pack(anchor=tk.W, pady=2)
        
        ttk.Checkbutton(right_options, text="Eliminar caracteres especiales", 
                       variable=self.remove_special_var, command=self.update_preview).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(right_options, text="Preservar números (0-9)", 
                       variable=self.preserve_numbers_var, command=self.update_preview).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(right_options, text="Preservar puntos (.)", 
                       variable=self.preserve_dots_var, command=self.update_preview).pack(anchor=tk.W, pady=2)
        
        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        
        self.preview_btn = ttk.Button(buttons_frame, text="👁️ Vista Previa", 
                                    command=self.show_preview, style="Accent.TButton")
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.examples_btn = ttk.Button(buttons_frame, text="📋 Ver Ejemplos", 
                                     command=self.show_examples)
        self.examples_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.rename_btn = ttk.Button(buttons_frame, text="🔄 Renombrar Carpetas", 
                                   command=self.start_rename_process, style="Accent.TButton")
        self.rename_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.help_btn = ttk.Button(buttons_frame, text="❓ Ayuda", command=self.show_help)
        self.help_btn.pack(side=tk.LEFT)
        
        # Área de resultados con pestañas
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Pestaña de vista previa
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="Vista Previa")
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=15, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de log de resultados
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="Log de Resultados")
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo - Selecciona un directorio para comenzar")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Inicializar con directorio actual
        self.use_current_directory()
        
    def apply_modern_theme(self):
        """Aplica un tema moderno a la interfaz"""
        style = ttk.Style()
        
        # Configurar tema
        if "clam" in style.theme_names():
            style.theme_use("clam")
        
        # Personalizar colores
        style.configure("Accent.TButton", 
                       background="#0078d4", 
                       foreground="white",
                       font=("Segoe UI", 9, "bold"))
        
    def browse_directory(self):
        """Abre el diálogo para seleccionar directorio"""
        directory = filedialog.askdirectory(title="Seleccionar directorio de trabajo")
        if directory:
            self.directory_var.set(directory)
            self.update_status(f"Directorio seleccionado: {directory}")
            self.update_preview()
            
    def use_current_directory(self):
        """Usa el directorio actual del ejecutable"""
        if getattr(sys, 'frozen', False):
            current_dir = os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.directory_var.set(current_dir)
        self.update_status(f"Usando directorio actual: {current_dir}")
        self.update_preview()
        
    def get_options(self):
        """Obtiene las opciones actuales de configuración"""
        return {
            'lowercase': self.lowercase_var.get(),
            'remove_accents': self.remove_accents_var.get(),
            'replace_spaces': self.replace_spaces_var.get(),
            'remove_special': self.remove_special_var.get(),
            'preserve_numbers': self.preserve_numbers_var.get(),
            'preserve_dots': self.preserve_dots_var.get()
        }
        
    def normalize_folder_name(self, name, options=None):
        """Normaliza el nombre de la carpeta según las opciones especificadas"""
        if not name or not isinstance(name, str):
            return 'unnamed_folder'
        
        if options is None:
            options = self.get_options()
        
        original_name = name
        
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
        
    def update_preview(self):
        """Actualiza la vista previa automáticamente"""
        if self.directory_var.get():
            self.show_preview()
            
    def show_preview(self):
        """Muestra una vista previa de los cambios que se realizarán"""
        directory = self.directory_var.get()
        if not directory:
            messagebox.showwarning("Advertencia", "Por favor selecciona un directorio primero.")
            return
            
        try:
            base_path = Path(directory).resolve()
            
            if not base_path.exists():
                self.update_status("ERROR: El directorio no existe")
                return
                
            if not base_path.is_dir():
                self.update_status("ERROR: La ruta no es un directorio")
                return
            
            folders = [item for item in base_path.iterdir() if item.is_dir()]
            
            if not folders:
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(tk.END, "ℹ️ No se encontraron carpetas en este directorio.")
                self.update_status("No hay carpetas para procesar")
                return
            
            options = self.get_options()
            self.preview_data = []
            
            # Generar vista previa
            preview_content = f"📂 VISTA PREVIA - {len(folders)} carpetas encontradas\n"
            preview_content += f"📍 Directorio: {base_path}\n"
            preview_content += "═" * 80 + "\n\n"
            
            changes_count = 0
            conflicts_count = 0
            
            for i, folder in enumerate(folders, 1):
                original_name = folder.name
                new_name = self.normalize_folder_name(original_name, options)
                
                status = ""
                if original_name == new_name:
                    status = "✅ Sin cambios"
                else:
                    new_path = folder.parent / new_name
                    if new_path.exists():
                        status = "⚠️ CONFLICTO (ya existe)"
                        conflicts_count += 1
                    else:
                        status = "🔄 Se renombrará"
                        changes_count += 1
                
                preview_line = f"[{i:2d}] {status}\n"
                preview_line += f"     '{original_name}'\n"
                if original_name != new_name:
                    preview_line += f"  → '{new_name}'\n"
                preview_line += "\n"
                
                preview_content += preview_line
                
                self.preview_data.append({
                    'folder': folder,
                    'original_name': original_name,
                    'new_name': new_name,
                    'will_change': original_name != new_name,
                    'has_conflict': new_path.exists() if original_name != new_name else False
                })
            
            # Resumen
            summary = f"\n{'='*80}\n"
            summary += f"📊 RESUMEN:\n"
            summary += f"   • Total de carpetas: {len(folders)}\n"
            summary += f"   • Se renombrarán: {changes_count}\n"
            summary += f"   • Sin cambios: {len(folders) - changes_count - conflicts_count}\n"
            if conflicts_count > 0:
                summary += f"   • ⚠️ Conflictos: {conflicts_count}\n"
            
            preview_content += summary
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, preview_content)
            
            self.update_status(f"Vista previa generada: {changes_count} cambios, {conflicts_count} conflictos")
            
        except Exception as e:
            self.update_status(f"Error al generar vista previa: {str(e)}")
            messagebox.showerror("Error", f"Error al generar vista previa:\n{str(e)}")
            
    def show_examples(self):
        """Muestra ejemplos de transformación en una ventana nueva"""
        examples_window = tk.Toplevel(self.root)
        examples_window.title("Ejemplos de Transformación")
        examples_window.geometry("600x500")
        examples_window.transient(self.root)
        examples_window.grab_set()
        
        frame = ttk.Frame(examples_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(frame, text="📋 Ejemplos de Transformación", 
                               font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        examples_text = scrolledtext.ScrolledText(frame, height=20, wrap=tk.WORD)
        examples_text.pack(fill=tk.BOTH, expand=True)
        
        options = self.get_options()
        
        examples = [
            "Mi Carpeta Especial ñáéíóú",
            "Fotos Vacaciones (2024)",
            "Música - Rock & Roll",
            "DOCUMENTOS IMPORTANTES!!!",
            "Nueva Carpeta 1.5",
            "Proyecto Final - Versión 2.0",
            "Diseño Gráfico & Animación",
            "Datos Científicos [Backup]",
            "Películas HD (1080p)",
            "Código Fuente - Python 3.9"
        ]
        
        content = "Con la configuración actual:\n\n"
        
        for i, example in enumerate(examples, 1):
            transformed = self.normalize_folder_name(example, options)
            content += f"{i:2d}. '{example}'\n"
            content += f"    → '{transformed}'\n\n"
        
        examples_text.insert(tk.END, content)
        examples_text.configure(state='disabled')
        
        close_btn = ttk.Button(frame, text="Cerrar", command=examples_window.destroy)
        close_btn.pack(pady=(10, 0))
        
    def start_rename_process(self):
        """Inicia el proceso de renombrado en un hilo separado"""
        if not self.preview_data:
            messagebox.showwarning("Advertencia", "Por favor genera una vista previa primero.")
            return
            
        # Verificar si hay cambios que hacer
        changes = [item for item in self.preview_data if item['will_change'] and not item['has_conflict']]
        conflicts = [item for item in self.preview_data if item['has_conflict']]
        
        if not changes:
            if conflicts:
                messagebox.showinfo("Sin cambios", 
                                  f"No hay cambios que realizar.\nSe detectaron {len(conflicts)} conflictos que deben resolverse manualmente.")
            else:
                messagebox.showinfo("Sin cambios", "No hay cambios que realizar. Todas las carpetas ya tienen nombres normalizados.")
            return
        
        # Confirmar la operación
        message = f"¿Confirmas que quieres renombrar {len(changes)} carpetas?"
        if conflicts:
            message += f"\n\nNOTA: {len(conflicts)} carpetas con conflictos serán omitidas."
        
        if not messagebox.askyesno("Confirmar Renombrado", message):
            return
            
        # Deshabilitar botones durante el proceso
        self.rename_btn.configure(state='disabled')
        self.preview_btn.configure(state='disabled')
        
        # Ejecutar en hilo separado para no bloquear la interfaz
        threading.Thread(target=self.rename_folders_thread, daemon=True).start()
        
    def rename_folders_thread(self):
        """Ejecuta el renombrado en un hilo separado"""
        try:
            self.log_text.delete(1.0, tk.END)
            
            log_content = f"🔄 INICIANDO PROCESO DE RENOMBRADO\n"
            log_content += f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            log_content += f"📂 Directorio: {self.directory_var.get()}\n"
            log_content += "═" * 80 + "\n\n"
            
            self.root.after(0, lambda: self.log_text.insert(tk.END, log_content))
            self.root.after(0, lambda: self.update_status("Renombrando carpetas..."))
            
            renamed_count = 0
            skipped_count = 0
            error_count = 0
            
            for i, item in enumerate(self.preview_data, 1):
                if not item['will_change']:
                    log_line = f"[{i:2d}] ✅ Sin cambios: '{item['original_name']}'\n"
                    skipped_count += 1
                elif item['has_conflict']:
                    log_line = f"[{i:2d}] ⚠️ CONFLICTO: '{item['original_name']}' → '{item['new_name']}' (ya existe)\n"
                    error_count += 1
                else:
                    try:
                        new_path = item['folder'].parent / item['new_name']
                        item['folder'].rename(new_path)
                        log_line = f"[{i:2d}] 🔄 RENOMBRADO: '{item['original_name']}' → '{item['new_name']}'\n"
                        renamed_count += 1
                    except Exception as e:
                        log_line = f"[{i:2d}] ❌ ERROR: '{item['original_name']}' - {str(e)}\n"
                        error_count += 1
                
                self.root.after(0, lambda line=log_line: self.log_text.insert(tk.END, line))
                self.root.after(0, lambda: self.log_text.see(tk.END))
            
            # Resumen final
            summary = f"\n{'='*80}\n"
            summary += f"✅ PROCESO COMPLETADO\n\n"
            summary += f"📊 ESTADÍSTICAS FINALES:\n"
            summary += f"   • Carpetas renombradas: {renamed_count}\n"
            summary += f"   • Sin cambios: {skipped_count}\n"
            summary += f"   • Errores/Conflictos: {error_count}\n"
            summary += f"   • Total procesadas: {len(self.preview_data)}\n"
            
            self.root.after(0, lambda: self.log_text.insert(tk.END, summary))
            self.root.after(0, lambda: self.update_status(f"Completado: {renamed_count} renombradas, {error_count} errores"))
            
            # Mostrar mensaje de éxito
            if renamed_count > 0:
                self.root.after(0, lambda: messagebox.showinfo("Proceso Completado", 
                    f"✅ Proceso completado exitosamente!\n\n"
                    f"Carpetas renombradas: {renamed_count}\n"
                    f"Errores/Conflictos: {error_count}"))
            
            # Actualizar vista previa
            self.root.after(0, self.update_preview)
            
        except Exception as e:
            error_msg = f"❌ ERROR CRÍTICO: {str(e)}\n"
            self.root.after(0, lambda: self.log_text.insert(tk.END, error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error Crítico", f"Error durante el renombrado:\n{str(e)}"))
            
        finally:
            # Rehabilitar botones
            self.root.after(0, lambda: self.rename_btn.configure(state='normal'))
            self.root.after(0, lambda: self.preview_btn.configure(state='normal'))
            
    def show_help(self):
        """Muestra la ventana de ayuda"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda - Renombrador Universal")
        help_window.geometry("700x600")
        help_window.transient(self.root)
        help_window.grab_set()
        
        frame = ttk.Frame(help_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(frame, text="❓ Ayuda y Guía de Uso", 
                               font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        help_text = scrolledtext.ScrolledText(frame, height=25, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        
        help_content = """🎯 PROPÓSITO:
Este programa normaliza nombres de carpetas para hacerlos más compatibles con diferentes sistemas operativos, servidores web y aplicaciones.

📋 PASOS RECOMENDADOS:
1. Selecciona el directorio de trabajo usando "Examinar..." o "Usar Directorio Actual"
2. Configura las opciones según tus necesidades
3. Usa "Vista Previa" para ver qué cambios se realizarán
4. Si estás satisfecho con los cambios, haz clic en "Renombrar Carpetas"

⚙️ OPCIONES PRINCIPALES:

• Convertir a minúsculas: Convierte TODAS las letras a minúsculas
  Ejemplo: "MI CARPETA" → "mi carpeta"

• Eliminar acentos: Remueve tildes y caracteres especiales del español
  Ejemplo: "ñáéíóú" → "naeio"

• Reemplazar espacios: Convierte espacios en guiones bajos (_)
  Ejemplo: "mi carpeta" → "mi_carpeta"

• Eliminar caracteres especiales: Quita símbolos como @#$%&*()[]{}
  Ejemplo: "carpeta (2024)" → "carpeta_2024"

• Preservar números: Mantiene los dígitos del 0-9
  Ejemplo: "version 2.1" → "version_2_1" (si preservar puntos está desactivado)

• Preservar puntos: Mantiene los puntos en los nombres
  Ejemplo: "version 2.1" → "version_2.1"

🛡️ SEGURIDAD:
• Solo renombra CARPETAS, NO toca archivos
• No borra ni modifica el contenido de las carpetas
• Detecta conflictos de nombres antes de hacer cambios
• Muestra vista previa antes de hacer cualquier modificación

💡 CONSEJOS:
• Siempre haz una copia de seguridad antes de usar el programa
• Usa la vista previa para verificar los cambios antes de aplicarlos
• Resuelve manualmente los conflictos detectados antes de proceder
• Las carpetas que ya tienen nombres normalizados no serán modificadas

🚨 CONFLICTOS:
Un conflicto ocurre cuando el nuevo nombre ya existe. Por ejemplo:
- Tienes "Mi Carpeta" y "mi_carpeta"
- Ambas se normalizarían a "mi_carpeta"
- El programa detectará esto y no renombrará ninguna para evitar pérdida de datos

❓ ¿NECESITAS MÁS AYUDA?
Este programa es ideal para:
• Organizar archivos para servidores web
• Preparar carpetas para sistemas Linux
• Normalizar nombres para aplicaciones
• Eliminar caracteres problemáticos en nombres de archivos"""

        help_text.insert(tk.END, help_content)
        help_text.configure(state='disabled')
        
        close_btn = ttk.Button(frame, text="Cerrar", command=help_window.destroy)
        close_btn.pack(pady=(10, 0))
        
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_var.set(message)
        self.root.update_idletasks()

def main():
    """Función principal"""
    root = tk.Tk()
    
    # Configurar icono si existe
    try:
        # Si tenemos un icono, lo usamos
        pass
    except:
        pass
    
    app = RenombradorGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
