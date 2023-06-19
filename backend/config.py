import os

class Config:
    APP_NAME = "Bitespeed Identity Task"
    DB_URL = os.environ.get("DB_URL")
    SWAGGER_UI_URL = "/whereismyendpoint"