from backend.env import Environment

class Config:
    APP_NAME = "Bitespeed Identity Task"
    DB_URL = Environment.DB_URL
    SWAGGER_UI_URL = "/whereismyendpoint"