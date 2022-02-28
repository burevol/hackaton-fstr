#Хакатон ФСТР

##Развертывание на хостинге

###Docker-compose

####Формат файла .env

    FSTR_DB_HOST= #адрес БД
    FSTR_DB_PORT= #Порт БД 
    FSTR_LOGIN= #Логин БД
    FSTR_PASS=  #Пароль БД
    FSTR_DB_NAME= #Имя БД

#### Запуск
    docker-compose build
    docker-compose up -d

### Docker
     docker run -e FSTR_DB_HOST=127.0.0.1 -e FSTR_DB_PORT=5432 -e FSTR_LOGIN=postgres -e FSTR_PASS=postgres -p 8000:8000 hackaton-fstr:latest

#### Адрес интерфейса на хостинге 
    http://46.160.240.126:8000/submitData/
