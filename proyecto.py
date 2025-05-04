import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import json
import random

GUARDADO = "imagenes_guardadas.json"

class AlbumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💖 Mi Álbum de Recuerdos")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ffe6f0")
        self.root.resizable(True, True)

        self.imagenes = []
        self.cargar_fotos_guardadas()

        self.fondos_colores = ["#ffe6f0", "#e6f7ff", "#e6ffe6", "#fff5e6", "#f9e6ff"]

        self.menu_frame = tk.Frame(self.root, bg="#ffe6f0")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        self.crear_menu()

    def crear_menu(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        titulo = tk.Label(self.menu_frame, text="🌸 Mi Álbum de Recuerdos 🌸", bg="#ffe6f0", fg="#d63384",
                          font=("Comic Sans MS", 28, "bold"))
        titulo.pack(pady=30)

        self.crear_boton("📸 Agregar Foto", self.agregar_foto).pack(pady=10)
        self.crear_boton("📖 Ver Álbum", self.mostrar_album).pack(pady=10)
        self.crear_boton("🎨 Cambiar Fondo", self.cambiar_fondo).pack(pady=10)
        self.crear_boton("❌ Quitar Foto", self.quitar_foto).pack(pady=10)

        pie = tk.Label(self.menu_frame, text="✨ Hecho con amor para tus recuerdos ✨", bg="#ffe6f0", fg="#d63384",
                       font=("Comic Sans MS", 12, "italic"))
        pie.pack(side=tk.BOTTOM, pady=20)

    def crear_boton(self, texto, comando):
        return tk.Button(self.menu_frame, text=texto, command=comando,
                         bg="#ff66b2", fg="white", activebackground="#ff3385", activeforeground="white",
                         font=("Comic Sans MS", 16, "bold"), bd=0, relief=tk.FLAT, padx=20, pady=10,
                         highlightthickness=2, highlightbackground="#ffb3d9", cursor="hand2")

    def crear_boton_general(self, padre, texto, comando):
        return tk.Button(padre, text=texto, command=comando,
                         bg="#ff66b2", fg="white", activebackground="#ff3385", activeforeground="white",
                         font=("Comic Sans MS", 12, "bold"), bd=0, relief=tk.FLAT, padx=15, pady=8,
                         highlightthickness=2, highlightbackground="#ffb3d9", cursor="hand2")

    def mostrar_album(self):
        self.menu_frame.destroy()

        self.album_frame = tk.Frame(self.root, bg=self.root.cget("bg"))
        self.album_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.album_frame, text="✨ Mi Álbum de Recuerdos ✨", font=("Comic Sans MS", 24, "bold"), fg="#d63384", bg=self.root.cget("bg")).pack(pady=20)

        self.index = 0
        if self.imagenes:
            self.mostrar_hoja(self.imagenes[self.index])
        else:
            self.mostrar_hoja_de_fin()

    def mostrar_hoja(self, ruta):
        try:
            for widget in self.album_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()

            ventana_hoja = tk.Frame(self.album_frame, bg="white", bd=10, relief="solid", highlightbackground="#ff66b2", highlightthickness=3)
            ventana_hoja.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

            img = Image.open(ruta)
            width, height = img.size

            window_width = 800
            window_height = 500

            ratio = min(window_width / width, window_height / height)
            img = img.resize((int(width * ratio), int(height * ratio)), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(ventana_hoja, image=img_tk, bg="white")
            img_label.image = img_tk
            img_label.pack(padx=20, pady=20)

            titulo = f"📷 {os.path.basename(ruta)}"
            tk.Label(ventana_hoja, text=titulo, font=("Comic Sans MS", 14, "bold"), fg="#d63384", bg="white").pack(pady=10)

            # Panel de botones
            control_frame = tk.Frame(self.album_frame, bg=self.root.cget("bg"))
            control_frame.pack(pady=10)

            self.crear_boton_general(control_frame, "⬅️ Anterior", self.anterior_hoja).pack(side=tk.LEFT, padx=10)
            self.crear_boton_general(control_frame, "➡️ Siguiente", self.siguiente_hoja).pack(side=tk.LEFT, padx=10)
            self.crear_boton_general(control_frame, "🎨 Fondo", self.cambiar_fondo).pack(side=tk.LEFT, padx=10)
            self.crear_boton_general(control_frame, "🏠 Menú", self.volver_al_menu).pack(side=tk.LEFT, padx=10)

        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def siguiente_hoja(self):
        self.index += 1
        if self.index >= len(self.imagenes):
            self.mostrar_hoja_de_fin()
            return

        self.mostrar_hoja(self.imagenes[self.index])

    def anterior_hoja(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
        self.mostrar_hoja(self.imagenes[self.index])

    def mostrar_hoja_de_fin(self):
        for widget in self.album_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        ventana_hoja = tk.Frame(self.album_frame, bg="white", bd=10, relief="solid", highlightbackground="#ff66b2", highlightthickness=3)
        ventana_hoja.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        label = tk.Label(ventana_hoja, text="✨ No hay más fotos... ¡Agrega más para seguir viendo! ✨",
                         font=("Comic Sans MS", 16, "bold"), fg="#d63384", bg="white", wraplength=750)
        label.pack(padx=20, pady=20)

        control_frame = tk.Frame(self.album_frame, bg=self.root.cget("bg"))
        control_frame.pack(pady=10)

        self.crear_boton_general(control_frame, "🏠 Menú", self.volver_al_menu).pack(side=tk.LEFT, padx=10)

    def volver_al_menu(self):
        self.album_frame.destroy()
        self.menu_frame = tk.Frame(self.root, bg=self.root.cget("bg"))
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        self.crear_menu()

    def agregar_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.guardar_foto(ruta)
            self.imagenes.append(ruta)
            self.mostrar_confirmacion("Foto agregada correctamente!")

    def quitar_foto(self):
        if not self.imagenes:
            self.mostrar_confirmacion("No hay fotos para quitar")
            return

        ruta = self.imagenes.pop()
        self.guardar_lista()
        self.mostrar_confirmacion(f"Foto {os.path.basename(ruta)} quitada!")

    def cambiar_fondo(self):
        nuevo_color = random.choice(self.fondos_colores)
        self.root.configure(bg=nuevo_color)
        if hasattr(self, 'menu_frame'):
            self.menu_frame.configure(bg=nuevo_color)
            for widget in self.menu_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=nuevo_color)

        if hasattr(self, 'album_frame'):
            self.album_frame.configure(bg=nuevo_color)
            for widget in self.album_frame.winfo_children():
                if isinstance(widget, tk.Label) or isinstance(widget, tk.Frame):
                    widget.configure(bg=nuevo_color)

    def guardar_foto(self, ruta):
        fotos = []
        if os.path.exists(GUARDADO):
            with open(GUARDADO, "r") as f:
                fotos = json.load(f)

        if ruta not in fotos:
            fotos.append(ruta)
            with open(GUARDADO, "w") as f:
                json.dump(fotos, f)

    def guardar_lista(self):
        with open(GUARDADO, "w") as f:
            json.dump(self.imagenes, f)

    def cargar_fotos_guardadas(self):
        if os.path.exists(GUARDADO):
            with open(GUARDADO, "r") as f:
                fotos = json.load(f)
                for ruta in fotos:
                    if os.path.exists(ruta):
                        self.imagenes.append(ruta)
        else:
            with open(GUARDADO, "w") as f:
                json.dump([], f)

    def mostrar_confirmacion(self, mensaje):
        ventana_confirmacion = tk.Toplevel(self.root)
        ventana_confirmacion.title("✅ Confirmación")
        ventana_confirmacion.geometry("300x150")
        ventana_confirmacion.configure(bg="#ffe6f0")

        tk.Label(ventana_confirmacion, text=mensaje, font=("Comic Sans MS", 14), fg="#d63384", bg="#ffe6f0").pack(pady=20)
        tk.Button(ventana_confirmacion, text="Cerrar", command=ventana_confirmacion.destroy,
                  bg="#ff66b2", fg="white", activebackground="#ff3385", activeforeground="white",
                  font=("Comic Sans MS", 12, "bold"), bd=0, relief=tk.FLAT, padx=10, pady=5,
                  highlightthickness=2, highlightbackground="#ffb3d9", cursor="hand2").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AlbumApp(root)
    root.mainloop()