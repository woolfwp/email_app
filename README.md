**Descripción de la Aplicación**

La aplicación desarrollada es una aplicación web basada en Flask que permite gestionar bases de datos y enviar correos electrónicos a los administradores cuando la criticidad de una base de datos es alta. 
La aplicación está diseñada para ser ejecutada en un entorno Dockerizado, lo que facilita su despliegue y mantenimiento en diferentes plataformas.

**Instrucciones para la Ejecución de la Aplicación**

Para ejecutar la aplicación, sigue los siguientes pasos:

1. Clonar el Repositorio: Clona el repositorio de la aplicación desde GitHub o copia los archivos en tu máquina local.

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. Instalar Dependencias: Asegúrate de tener Docker instalado en tu máquina. 
3. Construir la Imagen Docker: En la raíz del proyecto donde se encuentra tu Dockerfile, ejecuta el siguiente comando para construir la imagen de Docker:

   ```bash
   docker build -t mi_proyecto:latest .
   ```

4. Ejecutar el Contenedor Docker: Una vez construida la imagen, ejecuta el siguiente comando para iniciar el contenedor Docker:

   ```bash
   docker run -p 5000:5000 --env-file .env mi_proyecto:latest
   ```

5. Acceder a la Aplicación: Abre un navegador web y navega a `http://localhost:5000` (o la dirección IP de tu máquina si estás utilizando Docker Toolbox en Windows o macOS).

**Uso de Docker**

La aplicación está contenerizada usando Docker para facilitar la implementación y el despliegue en diferentes entornos. 
El Dockerfile incluido define la configuración del contenedor, incluyendo las dependencias y la configuración de Flask. 
Se usa un archivo `.env` para la configuración de variables de entorno necesarias para la aplicación.

**Supuestos, Problemas y Soluciones**

Durante el desarrollo de la aplicación, se encontraron algunos desafíos relacionados con la configuración de red, la integración de servicios externos como SMTP para el envío de correos electrónicos
y la gestión de la criticidad de las bases de datos. Estos problemas se resolvieron mediante pruebas exhaustivas, ajustes en la configuración de Docker y optimizaciones en el código Python de Flask.

**Conclusiones**

Esta documentación proporciona una guía básica sobre cómo ejecutar la aplicación utilizando Docker, así como detalles sobre su integración y los desafíos encontrados durante el desarrollo. 


