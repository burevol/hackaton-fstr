FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ARG FSTR_DB_HOST
ARG FSTR_DB_PORT
ARG FSTR_LOGIN
ARG FSTR_PASS
ARG FSTR_DB_NAME

ENV FSTR_DB_HOST=$FSTR_DB_HOST
ENV FSTR_DB_PORT=$FSTR_DB_PORT
ENV FSTR_LOGIN=$FSTR_LOGIN
ENV FSTR_PASS=$FSTR_PASS
ENV FSTR_DB_NAME=$FSTR_DB_NAME

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "main:app" , "--reload", "--host", "0.0.0.0"]

