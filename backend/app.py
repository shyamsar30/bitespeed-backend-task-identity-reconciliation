import json
import traceback
from flask import Flask, g, redirect
from flask_restx import Api
from sqlalchemy import text

from backend.api.responses import handle_exceptions
from backend.config import Config
from backend.database.connector import db_session
from backend.api.endpoints import namespace

# To be executed before any request
def before_request():
    g.db_session = db_session()


# Setup Swagger UI
class ExtendedApi(Api):
    @property
    def specs_url(self):
        return f"{Config.SWAGGER_UI_URL}/swagger.json"
    
    def init_app(self, app, *args, **kwargs):
        app.route(f"{Config.SWAGGER_UI_URL}/swagger.json")(lambda: json.dumps(self.__schema__))
        super().init_app(app, *args, **kwargs)


# Configuring endpoints to Swagger
def configure_endpoints(app):
    restx_api = ExtendedApi(
        title="Bitespeed Task Identity",
        version="1.0",
        description="API Documentation of apis.",
        doc=Config.SWAGGER_UI_URL,
        prefix="/api"
    )

    restx_api.add_namespace(namespace)

    restx_api.init_app(app)
    
    app.before_request(before_request)
    app.register_error_handler(Exception, handle_exceptions)

    return app


# Configuring Database and checking connection
def configure_database(app):
    try:
        db_session.execute(text("SELECT 1;"))
    except Exception as e:
        traceback.print_exc()
        raise e


# Flask App Setup
def init_app():
    app = Flask(Config.APP_NAME)

    configure_endpoints(app)
    configure_database(app)

    app.config['DEBUG'] = True

    @app.route('/')
    def home():
        return redirect(Config.SWAGGER_UI_URL)

    return app


app = init_app()
app.run(debug=True)