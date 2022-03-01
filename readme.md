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