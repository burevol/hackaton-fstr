import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from utils import Item, send_data

app = FastAPI()


class OperationException(Exception):
    pass


class BadRequestException(Exception):
    pass


@app.post("/submitData/")
async def submit_data(item: Item):
    try:
        id = send_data(jsonable_encoder(item))
    except OperationException as ex:
        return JSONResponse({'status': 503, 'message': ex.args[0]})
    except BadRequestException as ex:
        return JSONResponse({'status': 400, 'message': ex.args[0]})
    else:
        return JSONResponse({'status': 200, 'message': 'Отправлено успешно', 'id': id})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'status': 400,
                                  "message": 'Ошибка формата сообщения',
                                  }),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
