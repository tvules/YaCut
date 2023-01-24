FROM python:3.9-slim

WORKDIR /app

COPY /yacut ./yacut
COPY /migrations ./migrations
COPY requirements.txt ./
COPY settings.py ./

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && gunicorn -b :5000 yacut:app"]
