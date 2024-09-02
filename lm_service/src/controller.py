import logging
from src.constants import HTTPConstants as CODES
from src.constants import ModelConstants as MC
from src.constants import ArgTypes as AT
from src.model_handler import SmallLM
from src.validation import Arg, Args
from flask import Blueprint, jsonify, make_response, request

main = Blueprint("main", __name__)


@main.before_request
def before_request():
    """
    Used to set CORS headers before any request
    """
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    if request.method.lower() == "options":
        return response, 200


@main.route("/models", methods=["GET"])
def models():
    """
    Returns a list of available models to use
    """
    return jsonify(MC.AVAILABLE_MODELS)


@main.route("/predict", methods=["POST"])
def predict():
    """
    Returns the response of the specified model with the specified prompt
    """
    model_name = request.json.get("model_name", None)
    prompt = request.json.get("prompt", None)
    sys_msg = request.json.get("sys_msg", None)
    
    request_params = [
        Arg(model_name, AT.STR, "model_name"),
        Arg(prompt, AT.STR, "prompt"),
        Arg(sys_msg, AT.STR, "sys_msg", required=False),
    ]

    # Parse request's parameters
    if invalid_arg := Args(request_params).get_invalid():
        return (
            jsonify({"error": f"Invalid argument {invalid_arg.name}={invalid_arg.value}"}),
            CODES.BAD_REQUEST,
        )

    # Check if the model exists
    if model_name not in MC.MODELS.keys():
        return (
            jsonify({"error": f"Model {model_name} not found"}),
            CODES.NOT_FOUND,
        )
    # Get the prediction from the model
    try:
        response = {"prediction": SmallLM(model_name).generate(prompt, sys_msg)}
        return_code = CODES.OK
    except Exception:
        response = {"error": "Unable to get a prediction"}
        return_code = CODES.SERVER_ERROR
        logging.error("An error occurred when trying to get a prediction", exc_info=True)

    return jsonify(response), return_code
