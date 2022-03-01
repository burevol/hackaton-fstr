import psycopg2
import requests
import uvicorn
import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utils import Item, send_data, send_image, get_status

app = FastAPI()


@app.post("/submitData/")
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

@app.get("/submitData/{data_id}/status/")
async def get_status(data_id: int):
    """Get status of selected data instance"""
    status = get_status(data_id)
    return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                {'status': 200, 'id': status}))


@app.get("/submitData/{data_id}", response_model=Item)
async def get_data(data_id: int):
    """Get data by id"""
    pass

@app.get("/submitData/")
async def get_data_by_user(fio: str = None, telephone: str = None, mail:str = None):
    """Get data by filter"""
    pass

@app.put("/submitData/{data_id}", response_model=Item)
async def put_data(data_id: int):
    """Changet the selected data"""
    pass




@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.info(exc.args[0])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'status': 400,
                                  "message": 'Ошибка формата сообщения',
                                  }),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
