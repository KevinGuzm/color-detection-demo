# Utiliza una imagen base de Python ligera
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación al contenedor
COPY . .

# Expone el puerto que utiliza tu aplicación (si es necesario)
EXPOSE 5000

# Comando para ejecutar tu aplicación
CMD ["python", "app.py"]
