import requests

from src.constants import HTTPCodes as CODES
from src.constants import ModelConstants as MC
from src.validation import Characters, Character


class ModelInterface:
    """
    Class used as an interface between the language model service and the API
    """

    def __init__(self, model_name: str = MC.DEFAULT_MODEL):
        self.model_name = model_name
        self.model_api_url = MC.API_URL

    def create_story(self, characters: Characters, setting: str, theme: str, genre: str):
        """
        Creates a story with the given details

        Args:
            characters (Characters): Characters to be included in the story
            setting (str): Where the story takes place
            theme (str): What the story should be about
            genre (str): Genre of the story

        Returns:
            (str, int): Generated text by the model and HTTP status code
        """
        prompt = f"The genre of the story is: {genre}. "
        prompt += f"The story is about: {theme}. "
        prompt += f"The story takes place in {setting}. "
        prompt += "Here is the description of the characters: "
        # Remove possible duplicated characters by creating a set of characters
        characters.set_characters()
        for character in characters.characters:
            prompt += f"The character '{character.name}' is a {character.role}."
            prompt += f"They are a {','.join(trait for trait in character.traits)} character. "

        sys_msg = MC.STORY_PROMPT

        prediction, status = self.get_prediction(prompt, sys_msg)  # TODO: this request times out :(
        prediction = prediction.strip().strip("\n")
        return prediction, status

    def fix_spelling(self, text: str):
        """
        Fixes the spelling of any given text.

        Args:
            text (str): Text with potential spelling mistakes

        Returns:
            (str, int): Generated text by the model and HTTP status code
        """
        sys_msg = MC.FIX_SPELLING_PROMPT
        prediction, status = self.get_prediction(text, sys_msg)
        prediction = prediction.replace(MC.SPELLING_ANSWER_PREFIX, "").strip().strip("\n")
        return prediction, status

    def translate(self, text: str, language: str):
        """
        Translates any given text into the specified language

        Args:
            text (str): Text to be translated
            language (str): Language to translate the text to

        Returns:
            (str, int): Generated text by the model and HTTP status code
        """
        # Note: it is not clear what languages the model handles,
        # so the quality of the results will depend highly on the language.
        sys_msg = MC.TRANSLATE_PROMPT.format(language=language)
        prediction, status = self.get_prediction(text, sys_msg)
        prediction = prediction.strip().strip("\n")
        return prediction, status

    def get_prediction(self, prompt: str, sys_msg: str = ""):
        """
        Makes an HTTP request to the language model microservice to make
        an inference with the given prompt

        Args:
            prompt (str): Text provided by the user
            sys_msg (str, optional): System messages to provide as context \
                for the model. Defaults to "".

        Returns:
            _type_: _description_
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        json_data = {
            "model_name": self.model_name,
            "prompt": prompt,
            "sys_msg": sys_msg,
        }

        response = requests.post(
            self.model_api_url + MC.PREDICTION_ENDPOINT, headers=headers, json=json_data
        )

        if response.status_code != CODES.OK:
            return "", CODES.SERVER_ERROR

        return response.json()["prediction"], CODES.OK
