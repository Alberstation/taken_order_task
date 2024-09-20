# taken_order_classifier

Este proyecto tiene el propósito de realizar una clasificación sobre órdenes de compra para visualizar si han sido tomadas o no.


## Archivos

- requirements.txt: Librerias requeridas para la ejecución del proyecto
- Predictions.log: Logs del proyecto con la librería logging de python
- Prueba_RAPPI.ipynb: Jupyter notebook con la construcción del modelo
- PARTE 1 PRUEBA.pdf: pdf con descripción la tarea 1

app/
- main.py: codigo fuente del despliegue streamlit

app/models/
- manage_model.py: codigo fuente de la preparación de datos y ejecuciones del modelo
- modelo_decision_tree.pkl: ejecutable del modelo de clasificación
- pipeline.pkl: ejecutable del pipeline de preparación de datos

app/various_files/
- towns.txt: Archivo con todas las ciudades disponibles para usar el modelo
- image.png: Logo de Rappi


## Run

### Dockerfile

El archivo `Dockerfile` contiene las instrucciones necesarias para construir la imagen de la aplicación. Ejemplo:
```Dockerfile
# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos y el código
COPY requirements.txt .
COPY app/ /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Definir el comando por defecto
CMD ["python", "main.py"]

## Requisitos

Antes de empezar, asegúrate de tener instalados los siguientes programas en tu máquina:

- [Docker](https://www.docker.com/get-started) (versión 20.10.0 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versión 1.29.0 o superior)

## Ejecución
Inicia el contenedor:
Docker compose up -d --build

Detiene la aplicación:
Docker compsoe down 
