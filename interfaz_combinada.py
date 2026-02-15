import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import os
from analizador_sintactico import parsear_tokens, AnalizadorSintactico, imprimir_arbol

class AnalizadorCompletoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Lexico y Sintactico")
        self.root.geometry("900x700")
        
        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        
        main_frame = tk.Frame(root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # TÍTULO
        titulo = tk.Label(main_frame, 
                         text="Analizador Lexico y Sintactico",
                         font=("Arial", 16, "bold"),
                         bg=bg_color,
                         fg="#2c3e50")
        titulo.pack(pady=(0, 5))
        
        subtitulo = tk.Label(main_frame,
                            text="Ingresa expresiones matematicas o asignaciones (ej: x = 3 + 5)",
                            font=("Arial", 10),
                            bg=bg_color,
                            fg="#7f8c8d")
        subtitulo.pack(pady=(0, 15))
        
        # FRAME DE ENTRADA
        entrada_frame = tk.LabelFrame(main_frame,
                                      text="  Codigo Fuente  ",
                                      font=("Arial", 11, "bold"),
                                      bg=bg_color,
                                      fg="#34495e",
                                      padx=10,
                                      pady=10)
        entrada_frame.pack(fill=tk.BOTH, pady=(0, 10))
        
        self.entrada = scrolledtext.ScrolledText(entrada_frame,
                                                 height=5,
                                                 width=90,
                                                 font=("Consolas", 11),
                                                 wrap=tk.WORD,
                                                 borderwidth=2,
                                                 relief=tk.GROOVE)
        self.entrada.pack(padx=5, pady=5)
        
        ejemplo = "x = 3 + 5\ny = x * 2"
        self.entrada.insert("1.0", ejemplo)
        self.entrada.tag_add("ejemplo", "1.0", tk.END)
        self.entrada.tag_config("ejemplo", foreground="gray")
        
        self.entrada.bind("<FocusIn>", self.limpiar_ejemplo)
        self.es_ejemplo = True
        
        # BOTONES
        botones_frame = tk.Frame(main_frame, bg=bg_color)
        botones_frame.pack(pady=10)
        
        self.btn_analizar = tk.Button(botones_frame,
                                      text="▶ Analizar",
                                      command=self.analizar_completo,
                                      bg="#27ae60",
                                      fg="white",
                                      font=("Arial", 12, "bold"),
                                      width=15,
                                      height=1,
                                      cursor="hand2",
                                      relief=tk.RAISED,
                                      borderwidth=3)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(botones_frame,
                               text="Limpiar",
                               command=self.limpiar,
                               bg="#e74c3c",
                               fg="white",
                               font=("Arial", 12, "bold"),
                               width=15,
                               height=1,
                               cursor="hand2",
                               relief=tk.RAISED,
                               borderwidth=3)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # FRAME DE RESULTADOS (con dos columnas)
        resultados_frame = tk.Frame(main_frame, bg=bg_color)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        # Columna izquierda: Tokens
        tokens_frame = tk.LabelFrame(resultados_frame,
                                     text="  Analisis Lexico (Tokens)  ",
                                     font=("Arial", 10, "bold"),
                                     bg=bg_color,
                                     fg="#34495e",
                                     padx=10,
                                     pady=10)
        tokens_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.resultado_tokens = scrolledtext.ScrolledText(tokens_frame,
                                                          height=15,
                                                          width=40,
                                                          font=("Consolas", 10),
                                                          wrap=tk.WORD,
                                                          state='disabled',
                                                          borderwidth=2,
                                                          relief=tk.GROOVE,
                                                          bg="#ffffff")
        self.resultado_tokens.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Columna derecha: Árbol sintáctico
        arbol_frame = tk.LabelFrame(resultados_frame,
                                    text="  Analisis Sintactico (Arbol)  ",
                                    font=("Arial", 10, "bold"),
                                    bg=bg_color,
                                    fg="#34495e",
                                    padx=10,
                                    pady=10)
        arbol_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.resultado_arbol = scrolledtext.ScrolledText(arbol_frame,
                                                         height=15,
                                                         width=40,
                                                         font=("Consolas", 10),
                                                         wrap=tk.WORD,
                                                         state='disabled',
                                                         borderwidth=2,
                                                         relief=tk.GROOVE,
                                                         bg="#ffffff")
        self.resultado_arbol.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        # Footer
        footer = tk.Label(main_frame,
                         text="Analisis Lexico con Flex | Analisis Sintactico Descendente Recursivo",
                         font=("Arial", 8),
                         bg=bg_color,
                         fg="#95a5a6")
        footer.pack(side=tk.BOTTOM, pady=(10, 0))
        
        self.verificar_ejecutable()
    
    def limpiar_ejemplo(self, event):
        if self.es_ejemplo:
            self.entrada.delete("1.0", tk.END)
            self.entrada.tag_remove("ejemplo", "1.0", tk.END)
            self.es_ejemplo = False
    
    def verificar_ejecutable(self):
        if not os.path.exists("analizador.exe"):
            respuesta = messagebox.askyesno(
                "Analizador no encontrado",
                "No se encontro 'analizador.exe'.\n\n"
                "¿Deseas compilarlo ahora?\n\n"
                "Requiere Flex y GCC instalados"
            )
            if respuesta:
                self.compilar_analizador()
    
    def compilar_analizador(self):
        try:
            self.mostrar_tokens("⏳ Compilando...\n")
            self.root.update()
            
            resultado_flex = subprocess.run(
                ["flex", "analizador.l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if resultado_flex.returncode != 0:
                self.mostrar_tokens("Error en Flex:\n" + resultado_flex.stderr)
                return
            
            self.mostrar_tokens("Flex OK\n")
            self.root.update()
            
            resultado_gcc = subprocess.run(
                ["gcc", "lex.yy.c", "-o", "analizador.exe"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if resultado_gcc.returncode != 0:
                self.mostrar_tokens("Error en GCC:\n" + resultado_gcc.stderr)
                return
            
            self.mostrar_tokens("Compilacion exitosa\n")
            messagebox.showinfo("Analizador compilado correctamente")
            
        except FileNotFoundError:
            error_msg = (
                "No se encontro Flex o GCC\n\n"
                "Instala con: pacman -S flex gcc"
            )
            self.mostrar_tokens(error_msg)
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            self.mostrar_tokens(f"Error: {str(e)}")
    
    def analizar_completo(self):
        codigo = self.entrada.get("1.0", tk.END).strip()
        
        if not codigo or self.es_ejemplo:
            messagebox.showwarning("Advertencia", "Ingresa codigo para analizar")
            return
        
        if not os.path.exists("analizador.exe"):
            messagebox.showerror("Error", "Compila el analizador primero")
            self.verificar_ejecutable()
            return
        
        # PASO 1: Analisis Lexico
        try:
            with open("temp_input.txt", "w") as f:
                f.write(codigo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear archivo:\n{e}")
            return
        
        try:
            resultado = subprocess.run(
                ["./analizador.exe", "temp_input.txt"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            salida_lexico = resultado.stdout
            
            if not salida_lexico.strip():
                self.mostrar_tokens("Sin salida del lexico")
                self.mostrar_arbol("")
                return
            
            # Mostrar tokens
            self.mostrar_tokens(salida_lexico)
            
            # PASO 2: Analisis Sintactico
            tokens = parsear_tokens(salida_lexico)
            
            if not tokens:
                self.mostrar_arbol("No hay tokens para analizar")
                return
            
            analizador = AnalizadorSintactico(tokens)
            arbol, errores = analizador.analizar()
            
            # Mostrar resultado sintáctico
            if errores:
                resultado_sintactico = "ERRORES DE SINTAXIS:\n\n"
                for error in errores:
                    resultado_sintactico += f"  • {error}\n"
            else:
                resultado_sintactico = "SINTAXIS CORRECTA\n\n"
                resultado_sintactico += "Arbol Sintactico:\n\n"
                if arbol:
                    resultado_sintactico += imprimir_arbol(arbol)
                else:
                    resultado_sintactico += "(arbol vacio)"
            
            self.mostrar_arbol(resultado_sintactico)
                
        except FileNotFoundError:
            error_msg = "No se encontro analizador.exe"
            self.mostrar_tokens(error_msg)
            messagebox.showerror("Error", error_msg)
        except subprocess.TimeoutExpired:
            self.mostrar_tokens("Tiempo de espera agotado")
        except Exception as e:
            self.mostrar_tokens(f"Error: {str(e)}")
        finally:
            if os.path.exists("temp_input.txt"):
                try:
                    os.remove("temp_input.txt")
                except:
                    pass
    
    def limpiar(self):
        self.entrada.delete("1.0", tk.END)
        self.mostrar_tokens("")
        self.mostrar_arbol("")
        self.es_ejemplo = False
    
    def mostrar_tokens(self, texto):
        self.resultado_tokens.config(state='normal')
        self.resultado_tokens.delete("1.0", tk.END)
        self.resultado_tokens.insert("1.0", texto)
        self.resultado_tokens.config(state='disabled')
    
    def mostrar_arbol(self, texto):
        self.resultado_arbol.config(state='normal')
        self.resultado_arbol.delete("1.0", tk.END)
        self.resultado_arbol.insert("1.0", texto)
        self.resultado_arbol.config(state='disabled')

def main():
    root = tk.Tk()
    app = AnalizadorCompletoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()