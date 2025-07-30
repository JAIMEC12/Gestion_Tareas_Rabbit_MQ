# Especificar la imagen base para el contenedor
FROM python:3.11-slim
# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app
# Copiar todos los archivos del directorio actual (host) al contenedor
COPY . .
# Ejecutar comando para instalar dependencias de Python
RUN pip install pika
# Definir el comando por defecto que se ejecutará al iniciar el contenedor
CMD [ "python", "producer.py" ]
