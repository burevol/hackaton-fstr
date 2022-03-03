import json
import logging

import psycopg2
import requests
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utils import Item, send_data, send_image, get_status, get_data_by_id, get_filtered_data, update_data, Status, \
    Error, SubmitDataResponse

app = FastAPI()


@app.post("/submitData/",
          responses={
              200: {
                  "description": "Status of the posted record", "model": SubmitDataResponse
              },
              503: {
                  "description": "Database error", "model": Error
              },
              400: {
                  "description": "Validation error", "model": Error
              },
          }
          )
async def submit_data(item: Item):
    """Sends data from mobile app to database"""
    try:
        images_dict = {}
        for image in item.images:
            image_id = send_image(image.url)
            images_dict[image.title] = image_id

        pereval_id = send_data(jsonable_encoder(item), images_dict)
    except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.DataError) as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Ошибка работы с базой данных"}))
    except (requests.ConnectionError, requests.RequestException) as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Не удалось загрузить изображение"}))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                {'status': 200, 'message': 'Отправлено успешно', 'id': pereval_id}))


@app.get("/submitData/{data_id}/status/",
         responses={
             200: {
                 "description": "Status of the specified record", "model": Status
             },
             503: {
                 "description": "Database error", "model": Error
             },
             400: {
                 "description": "Validation error", "model": Error
             },
         }
         )
async def get_status_str(data_id: int):
    """Get status of selected data instance"""
    try:
        status_str = get_status(data_id)
    except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.DataError) as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Ошибка работы с базой данных"}))
    except TypeError as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Указанная запись не обнаружена"}))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                {'status': status_str}))


@app.get("/submitData/{data_id}", response_model=Item,
         responses={
             200: {
                 "description": "Raw data", "model": Item
             },
             503: {
                 "description": "Database error", "model": Error
             },
             400: {
                 "description": "Validation error", "model": Error
             },
         }
         )
async def get_data(data_id: int):
    """Get data by id"""
    try:
        raw_data = get_data_by_id(data_id)
    except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.DataError) as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Ошибка работы с базой данных"}))
    except TypeError as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Указанная запись не обнаружена"}))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(raw_data))


@app.get("/submitData/",
         responses={
             200: {
                 "description": "Raw data", "model": Item
             },
             503: {
                 "description": "Database error", "model": Error
             },
             400: {
                 "description": "Validation error", "model": Error
             },
         }
         )
async def get_data_by_user(fio: str = None, telephone: str = None, mail: str = None):
    """Get data by filter"""
    try:
        raw_data = get_filtered_data(fio, telephone, mail)
    except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.DataError) as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Ошибка работы с базой данных"}))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(raw_data))


@app.put("/submitData/{data_id}", response_model=Item,
         responses={
             200: {
                 "description": "Raw data", "model": Item
             },
             503: {
                 "description": "Database error", "model": Error
             },
             400: {
                 "description": "Validation error", "model": Error
             },
         }
         )
async def put_data(data_id: int, item: Item):
    """Change the selected data"""
    try:
        status_data = get_status(data_id)
        if status_data == 'new':
            raw_data = get_data_by_id(data_id)
            user_data = {
                "user": {"id": raw_data['user']['id'], "phone": raw_data['user']['id'],
                         'email': raw_data['user']['email']}}
            update_dict = item.dict()
            update_dict.update(user_data)
            update_data(data_id, json.dumps(update_dict))
    except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.DataError) as ex:
        logging.error(ex.args[0])
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=jsonable_encoder({'status': 503, 'message': "Ошибка работы с базой данных"}))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=json.dumps(update_dict))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(exc.args[0])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'status': 400,
                                  "message": 'Ошибка формата сообщения',
                                  }),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
