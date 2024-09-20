FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY app/* .

RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que correrá Streamlit
EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.enableCORS=false"]