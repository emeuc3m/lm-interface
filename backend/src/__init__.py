import logging
import datetime

from src.controller import main

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager


# Configure basic logging for the service
logging.basicConfig(
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} |--- {message}",
    style="{",
    datefmt="%d-%m-%H:%M:%S",
)

logging.root.setLevel(logging.INFO)


def create_app():
    """
    Creates, configures and returns a Flask app

    Returns:
        Flask: Flask app
    """
    app = Flask(__name__)
    app.register_blueprint(main)

    # Set CORS
    cors = CORS(app)

    # Configure JWT authentication
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_SECRET_KEY"] = "7BkXDrsiCXOv_AYF_1k"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=300)
    jwt = JWTManager(app)

    # Swagger configuration
    swagger_url = "/api/docs"
    api_url = "/static/swagger.yml"
    swagger_config = {"app_name": "lm-interface", "validatorUrl": None}
    swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, swagger_config)
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    return app
