from flask import Flask, request, render_template, redirect, url_for, flash
from enviar_emails import procesar_bases_de_datos
import webbrowser
import threading
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave secreta segura

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No se ha seleccionado ningún archivo.')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo.')
        return redirect(request.url)
    if file:
        filepath = os.path.join('bases_de_datos.json')
        file.save(filepath)
        flash('El archivo JSON ha sido cargado y procesado con éxito. Los Emails correspondientes fueron enviados')
        procesar_bases_de_datos(filepath)
        return redirect(url_for('index'))

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=False)
