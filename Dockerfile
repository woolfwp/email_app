# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos requirements.txt y .env al directorio de trabajo
COPY requirements.txt .
COPY .env .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto que usará la aplicación Flask
EXPOSE 5000

# Define la variable de entorno que le dice a Flask que se ejecute en modo producción
ENV FLASK_ENV=production

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
