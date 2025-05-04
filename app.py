from flask import Flask, render_template, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpeta donde se subirán las fotos
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta de inicio
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para el álbum de fotos
@app.route('/album')
def album():
    imagenes = cargar_fotos_guardadas()
    foto_id = request.args.get('id', 0, type=int)  # Tomamos el ID de la foto a mostrar
    foto_a_mostrar = imagenes[foto_id] if imagenes else None
    return render_template('album.html', imagenes=imagenes, foto_a_mostrar=foto_a_mostrar, foto_id=foto_id)

# Ruta para agregar foto
@app.route('/agregar_foto', methods=['GET', 'POST'])
def agregar_foto():
    if request.method == 'POST':
        if 'foto' not in request.files:
            return 'No hay archivo seleccionado'

        file = request.files['foto']
        if file.filename == '':
            return 'Nombre de archivo vacío'

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ruta_foto = url_for('static', filename=f'uploads/{filename}')
        guardar_foto(ruta_foto)
        return redirect(url_for('album'))

    return render_template('agregar_foto.html')

# Ruta para borrar foto
@app.route('/borrar_foto', methods=['GET', 'POST'])
def borrar_foto():
    if request.method == 'POST':
        foto = request.form['foto']
        quitar_foto_del_album(foto)
        return redirect(url_for('borrar_foto'))  # Volver a la misma página para actualizar la lista de fotos
    imagenes = cargar_fotos_guardadas()
    return render_template('borrar_foto.html', imagenes=imagenes)

def cargar_fotos_guardadas():
    # Función para cargar las fotos desde un archivo JSON
    if os.path.exists("fotos_guardadas.json"):
        with open("fotos_guardadas.json", "r") as f:
            return json.load(f)
    return []

def guardar_foto(foto):
    # Guardar foto en el archivo JSON
    imagenes = cargar_fotos_guardadas()
    if foto not in imagenes:
        imagenes.append(foto)
        with open("fotos_guardadas.json", "w") as f:
            json.dump(imagenes, f)

def quitar_foto_del_album(foto):
    # Quitar foto del álbum
    imagenes = cargar_fotos_guardadas()
    if foto in imagenes:
        imagenes.remove(foto)
        with open("fotos_guardadas.json", "w") as f:
            json.dump(imagenes, f)

if __name__ == '__main__':
    app.run(debug=True)
