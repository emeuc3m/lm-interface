class ModelConstants:
    """
    Class that contains all the constants related to the language models
    """

    MODELS_FOLDER = "src/language_models/"
    MODELS = {
        "llama-1.1b-chat": {
            "dir": "llama",
            "file": "tinyllama-1.1b-chat-v1.0.Q5_K_S.gguf",
            "template": "<|SYSTEM|>\n{context}</s>\n<|USER|>\n{prompt}</s>\n<|ASSISTANT|>\n",
        }
    }
    AVAILABLE_MODELS = [model for model in MODELS.keys()]


class HTTPConstants:
    """
    Class that contains all used HTTP codes
    """

    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500


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
