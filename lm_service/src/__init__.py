import logging
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from src.controller import main

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

    # Swagger configuration
    swagger_url = "/api/docs"
    api_url = "/static/swagger.yml"
    swagger_config = {"app_name": "lm-interface", "validatorUrl": None}
    swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, swagger_config)
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    return app
