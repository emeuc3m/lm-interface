class ModelConstants:
    """
    Class that contains all the constants related to the language models
    """

    API_URL = "http://lm_api_run:5000/"
    PREDICTION_ENDPOINT = "predict"
    DEFAULT_MODEL = "llama-1.1b-chat"

    TRANSLATE_PROMPT = (
        "Can you translate the following text to {language}? "
    )

    SPELLING_ANSWER_PREFIX = "Sure! Here is the corrected text:"
    FIX_SPELLING_PROMPT = (
        "You are a simple spelling corrector. "
        + "Your job is to correct the spelling errors and return an answer. "
        + f"The answer must start with '{SPELLING_ANSWER_PREFIX}'"
        + "Then the answer must contain the corrected text with no spelling errors. "
        + "Do not add quotes to the answer."
        + "If the spelling is already correct, your response should be the same text. "
        + "Please correct the spelling of the following text. "
    )

    STORY_PROMPT = (
        "You are a story teller."
        + "You must create a story that includes all the given characters. "
        + "The story must follow the given setting, tone and genre. "
        + "The length of the story must be less than 1000 words. "
        + "Do not be afraid of giving a long answer. "
        + "The story must have an ending. "
        + "Do not add quotes to the answer. "
        + "Your answer must contain exclusively the story. "
    )


class HTTPCodes:
    """
    Class that contains all used HTTP stauts codes
    """

    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500


class HTTPResponses:
    """
    Class that contains commonly used HTTP responses
    """

    FAILED_PREDICTION = {"error": "An error occurred while trying to process the prediction"}
    INVALID_JSON = {"error": "Provided parameter is not JSON valid"}


class ArgTypes:
    """
    Class that contains all available types for a request's parameters
    """

    INT = "int"
    FLOAT = "float"
    STR = "str"
    BOOL = "bool"
    LIST = "list"
    TUPLE = "tuple"
    SET = "set"
    DICT = "dict"
