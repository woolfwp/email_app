from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import webbrowser
import threading
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

load_dotenv()

# Definición de modelos
class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    manager_email = db.Column(db.String(255), unique=True, nullable=False)

class Database(db.Model):
    database_id = db.Column(db.Integer, primary_key=True)
    nombre_base_datos = db.Column(db.String(255), nullable=False)
    owner_email = db.Column(db.String(255), nullable=False)
    criticidad = db.Column(db.String(50))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'), nullable=False)
    manager = db.relationship('Manager', backref=db.backref('databases', lazy=True))

# Crear las tablas
with app.app_context():
    db.create_all()

def procesar_bases_de_datos(filepath):
    with open(filepath, 'r') as f:
        bases_de_datos = json.load(f)

    emails = []

    for db_data in bases_de_datos:
        nombre_base_datos = db_data.get('nombre_base_datos', 'Desconocido')
        email_manager = db_data.get('email_manager', 'No proporcionado')
        criticidad = db_data.get('criticidad', '').lower()
        owner_email = db_data.get('owner_email', 'No proporcionado')

        # Buscar o crear manager
        manager = Manager.query.filter_by(manager_email=email_manager).first()
        if not manager:
            manager = Manager(manager_email=email_manager)
            db.session.add(manager)
            db.session.commit()

        # Crear base de datos
        db_record = Database(nombre_base_datos=nombre_base_datos, owner_email=owner_email, criticidad=criticidad, manager_id=manager.manager_id)
        db.session.add(db_record)
        db.session.commit()

        if criticidad == 'alta' or criticidad == '':
            motivo = "La criticidad de la base de datos es alta. Por favor confirme."
            if criticidad == '':
                motivo = "La criticidad de la base de datos no está definida. Por favor proporcione una clasificación."
            emails.append({
                'nombre_base_datos': nombre_base_datos,
                'email_manager': email_manager,
                'criticidad': criticidad if criticidad else 'No definida',
                'motivo': motivo,
                'asunto': "Revisión de Criticidad de Base de Datos"
            })

    return emails

def enviar_email(email_manager, motivo):
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')

    # Imprime las variables para depuración
    print(f"from_email: {from_email}, from_password: {from_password}")

    if not from_email or not from_password:
        print("Error: Las credenciales de correo electrónico no se cargaron correctamente.")
        return

    print("Intentando enviar email...")
    print("Desde: ", from_email)
    print("Para: ", email_manager)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.starttls()
        server.login(from_email, from_password)
    except smtplib.SMTPAuthenticationError as e:
        print("Error de autenticación:", e)
        return
    except Exception as e:
        print("Error al conectar con el servidor SMTP:", e)
        return

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email_manager
    msg['Subject'] = "Revisión de Criticidad de Base de Datos"
    body = motivo
    msg.attach(MIMEText(body, 'plain'))

    try:
        server.sendmail(from_email, email_manager, msg.as_string())
        print("Correo enviado correctamente.")
    except Exception as e:
        print("Error al enviar correo:", e)
    finally:
        server.quit()

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
        flash('El archivo JSON ha sido cargado y procesado con éxito.')
        emails = procesar_bases_de_datos(filepath)
        for email in emails:
            enviar_email(email['email_manager'], email['motivo'])
        return redirect(url_for('index'))

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
