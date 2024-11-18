FROM python:3.12

WORKDIR /app

RUN pip install --no-cache-dir flask python-dotenv spotipy

COPY ./app .

CMD ["python3", "/app/main.py"]