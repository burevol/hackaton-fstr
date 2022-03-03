# Хакатон ФСТР

## Развертывание на хостинге

### Docker-compose

#### Формат файла .env

    FSTR_DB_HOST= #адрес БД
    FSTR_DB_PORT= #Порт БД 
    FSTR_LOGIN= #Логин БД
    FSTR_PASS=  #Пароль БД
    FSTR_DB_NAME= #Имя БД

#### Запуск
    docker-compose build
    docker-compose up -d

### Docker
     docker build -t hackaton-fstr:latest .
     docker run -e FSTR_DB_HOST=<адрес БД> -e FSTR_DB_PORT=<Порт БД> -e FSTR_LOGIN=<Логин БД> -e FSTR_PASS=<Пароль БД> -e FSTR_DB_NAME=<Имя БД> -p 8000:8000 hackaton-fstr:latest

#### Адрес интерфейса на хостинге 
    http://46.160.240.126:8000/submitData/
	
## Документация Swagger
    http://46.160.240.126:8000/docs

## Примеры вызова API

### POST /submitData
POST http://46.160.240.126:8000/submitData/

Данные:

{
  "beautyTitle": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": null,
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "type": "pass",
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "user": {
    "id": "vpupkin",
    "email": "user@email.tld",
    "phone": "79031234567",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович"
  },
  "images": [
    {
      "url": "https://www.imgonline.com.ua/examples/bee-on-daisy.jpg",
      "title": "Подъём. Фото №1"
    }
  ]
}

### GET /submitData/:id/status

GET http://46.160.240.126:8000/submitData/20/status

### GET /submitData/

GET http://46.160.240.126:8000/submitData?mail=user@email.tld

### GET /submitData/:id

GET http://46.160.240.126:8000/submitData/20

### PUT /submitData/:id

PUT http://46.160.240.126:8000/submitData/20

Данные:

{
  "beautyTitle": "пер. ",
  "title": "Пхия1",
  "other_titles": "Триев1",
  "connect": "",
  "add_time": null,
  "coords": {
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "type": "pass",
  "level": {
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "user": {
    "id": "vpupkin",
    "email": "user@email.tld",
    "phone": "79031234567",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович"
  },
  "images": [
    {
      "url": "https://www.imgonline.com.ua/examples/bee-on-daisy.jpg",
      "title": "Подъём. Фото №1"
    }
  ]
}
