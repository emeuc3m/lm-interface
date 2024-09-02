from constants import ModelConstants as MC
from ctransformers import AutoModelForCausalLM, AutoConfig

# model_path = os.path.join(os.getcwd(), "app", "model")
model_path = MC.MODELS["llama-2-7b-chat"]["path"]  # "TheBloke/Llama-2-7B-Chat-GGML"
model_file = MC.MODELS["llama-2-7b-chat"]["file"]
config = AutoConfig.from_pretrained(model_path, local_files_only=True)

print(model_path)
llm = AutoModelForCausalLM.from_pretrained(model_path, model_file=model_file, config=config)
print("Modelo cargado")


def get_prompt_with_template(characters: list, setting: str, theme: str, genre: str):
    prompt = f"The genre of the story is: {genre}. "
    prompt += f"The story is about: {theme}. "
    prompt += f"The story takes place in {setting}. "
    prompt += "Here is the description of the characters: "
    for character in characters:
        name = character["name"]
        role = character["role"]
        traits = ", ".join(trait for trait in character["traits"])
        prompt += f"The character '{name}' is a {role}. They are a {traits} character. "
    return (
        "[INST] <<SYS>>"
        "You are a story teller."
        "You must create a story that includes all the given characters. "
        "The story must follow the given setting, tone and genre. "
        "The length of the story must be less than 1000 words. "
        "Do not be afraid of giving a long answer. "
        "The story must have an ending. "
        "Do not add quotes to the answer. "
        "Your answer must contain exclusively the story. "
        f" <</SYS>>{prompt}[/INST]"
    )


characters = [
    {"name": "Aria", "role": "hero", "traits": ["brave", "kind"]},
    {"name": "Drako", "role": "villain", "traits": ["cunning", "ruthless"]},
]

setting = "A mystical forest in the kingdom of Eldoria, during a time of war"
theme = "The importance of friendship and loyalty"
genre = "fantasy"


prompt = get_prompt_with_template(characters, setting, theme, genre)
output = llm(prompt)
print(output)

# Translate X
# Spell Check X
# Summarize
# Complete text
# Question
# Chat ??
