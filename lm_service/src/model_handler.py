import logging
from src.constants import ModelConstants as MC
from ctransformers import AutoModelForCausalLM, AutoConfig


class SmallLM:
    """
    Class that interfaces a small language model
    """

    def __init__(self, model_name: str):
        # Get model information
        self.model_name = model_name
        self.model_path = MC.MODELS_FOLDER + MC.MODELS[model_name]["dir"]
        self.model_file = MC.MODELS[model_name]["file"]
        self.template = MC.MODELS[model_name]["template"]
        # Create config and load model
        self.model_config = AutoConfig.from_pretrained(self.model_path, local_files_only=True)
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path, model_file=self.model_file, config=self.model_config
            )
            logging.debug(f"Model {self.model_name} imported")
        except Exception:
            logging.error("Error importing model", exc_info=True)

    def generate(self, prompt: str, sys_msg: str = None):
        """
        Gets the model prediction with the given prompt

        Args:
            prompt (str): prompt for the model
            sys_msg (str, optional): Messages for the model to take as context before the
            actual prompt. Defaults to None.

        Returns:
            str: Text generated by the model
        """
        prompt = self.template.format(context=sys_msg, prompt=prompt)
        return self.model(prompt)
