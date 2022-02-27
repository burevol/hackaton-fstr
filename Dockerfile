FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "main:app" , "--reload", "--host", "0.0.0.0"]

