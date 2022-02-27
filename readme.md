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
