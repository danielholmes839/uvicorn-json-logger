import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from logger import UVICORN_LOGGING_CONFIG


app = FastAPI()


@app.get("/")
def index():
    return "Hello World!"


@app.get("/raise/{status_code}")
def exception(status_code: int):
    raise HTTPException(status_code)


if __name__ == "__main__":
    uvicorn.run(app, log_config=UVICORN_LOGGING_CONFIG)
