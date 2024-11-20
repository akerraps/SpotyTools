FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask spotipy

COPY ./app .

CMD ["python3", "/app/main.py"]