import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales del archivo .env
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Función para leer el archivo JSON
def leer_json(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

# Función para enviar un correo electrónico
def enviar_email(destinatario, asunto, mensaje):
    remitente = EMAIL_USER

    # Crear el objeto de mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Configurar el servidor SMTP
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remitente, EMAIL_PASSWORD)
    
    # Enviar el mensaje
    servidor.send_message(msg)
    servidor.quit()

# Función para procesar la base de datos y enviar correos
def procesar_bases_de_datos(filepath):
    # Leer la nueva base de datos
    nueva_base_de_datos = leer_json(filepath)

    # Revisar la criticidad y enviar correos según sea necesario
    for registro in nueva_base_de_datos:
        criticidad = registro["criticidad"].strip().lower()
        email_manager = registro["email_manager"]

        if criticidad == "alta":
            asunto = f"Revisión de criticidad alta para {registro['nombre_base_datos']}"
            mensaje = f"Estimado Manager,\n\nLa base de datos {registro['nombre_base_datos']} ha sido clasificada con una criticidad alta. Por favor, revise esta clasificación y confirme si es correcta.\n\nGracias."
            enviar_email(email_manager, asunto, mensaje)
            print(f"Correo enviado a {email_manager} respecto a {registro['nombre_base_datos']} con criticidad alta.")
        
        elif criticidad == "":
            asunto = f"Solicitud de criticidad para {registro['nombre_base_datos']}"
            mensaje = f"Estimado Manager,\n\nLa base de datos {registro['nombre_base_datos']} no tiene una criticidad asignada. Por favor, proporcione la criticidad correspondiente.\n\nGracias."
            enviar_email(email_manager, asunto, mensaje)
            print(f"Correo enviado a {email_manager} solicitando criticidad para {registro['nombre_base_datos']}.")

    print("Proceso completado.")

