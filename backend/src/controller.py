from src.constants import HTTPCodes as CODES
from src.constants import HTTPResponses as RESPONSES
from src.constants import ModelConstants as MC
from src.constants import ArgTypes as AT
from src.validation import Param, Characters, Args
from src.login_handler import validate_login
from src.lm_handler import ModelInterface

from flask import Blueprint, jsonify, make_response, request, Response
from flask_jwt_extended import create_access_token, jwt_required

main = Blueprint("main", __name__)


@main.before_request
def before_request():
    """
    Used for CORS preflight response
    """
    response = make_response()
    # Needed for CORS
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    if request.method.lower() == "options":
        return response, 200


def _corsify_actual_response(response: Response):
    """
    Sets up a response with CORS and Authorization headers

    Args:
        response (Response): Request's response

    Returns:
        Response: Response with correct headers
    """
    # Needed for CORS
    response.headers.add("Access-Control-Allow-Origin", "*")
    # Needed for JWT
    response.headers.add("Access-Control-Expose-Headers", "authorization")
    return response


def check_for_invalid_args(args: list):
    """
    Checks if any provided argument is not valid.

    Args:
        args (list): List of arguments

    Returns:
        Response, int: Response and status code if an invalidargument was found, None otherwise.

    """
    if invalid_arg := Args(args).get_invalid():
        return (
            _corsify_actual_response(
                jsonify({"error": f"Invalid parameter: {invalid_arg.name}={invalid_arg.value}"})
            ),
            CODES.BAD_REQUEST,
        )
    return None


@main.route("/login/", methods=["POST", "OPTIONS"])
def login():
    """
    Verifies user login and returns JWT token in Authorization header
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    request_params = [Param(username, AT.STR, "username"), Param(password, AT.STR, "password")]

    if response := check_for_invalid_args(request_params):
        return response

    if not validate_login(username, password):
        return _corsify_actual_response(jsonify({"error": "Incorrect username or password"})), 401

    response = make_response()
    access_token = create_access_token(identity=username)
    response.headers["Authorization"] = f"Bearer {access_token}"
    return _corsify_actual_response(response), 200


@main.route("/translate/", methods=["POST"])
@jwt_required()
def translate():
    """
    Translate a given text into the specified language
    """
    prompt_text = request.json.get("text", None)
    language = request.json.get("language", None)
    request_params = [Param(prompt_text, AT.STR, "text"), Param(language, AT.STR, "language")]
    if response := check_for_invalid_args(request_params):
        return response

    translation, status = ModelInterface().translate(prompt_text, language)
    if status == CODES.SERVER_ERROR:
        response = RESPONSES.FAILED_PREDICTION
    else:
        response = {"translation": translation}
    response = _corsify_actual_response(jsonify(response))
    return response, status


@main.route("/spelling/", methods=["POST"])
@jwt_required()
def spelling():
    """
    Corrects the spelling of any given text
    """
    prompt_text = request.json.get("text", None)
    request_params = [Param(prompt_text, AT.STR, "text")]
    if response := check_for_invalid_args(request_params):
        return response

    correction, status = ModelInterface().fix_spelling(prompt_text)

    if status == CODES.SERVER_ERROR:
        response = RESPONSES.FAILED_PREDICTION
    else:
        response = {"correction": correction}

    return _corsify_actual_response(jsonify(response)), status


@main.route("/story/", methods=["POST"])
@jwt_required()
def story():
    """
    Creates a story with the specified details
    """
    characters = Characters(request.json.get("characters", []))
    setting = request.json.get("setting", None)
    theme = request.json.get("theme", None)
    genre = request.json.get("genre", None)

    request_params = [
        characters,
        Param(setting, AT.STR, "setting"),
        Param(theme, AT.STR, "theme"),
        Param(genre, AT.STR, "genre"),
    ]

    if response := check_for_invalid_args(request_params):
        return response

    story, status = ModelInterface().create_story(characters, setting, theme, genre)

    if status == CODES.SERVER_ERROR:
        response = RESPONSES.FAILED_PREDICTION
    else:
        response = {"story": story}

    return _corsify_actual_response(jsonify(response)), status
