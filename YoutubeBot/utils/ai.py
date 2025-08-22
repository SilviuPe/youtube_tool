from openai import OpenAI
import os
import platform

from dotenv import load_dotenv

from .constants import STANDARD_PROMPT, STANDARD_MODEL, STANDARD_PROMPT_TITLE, STANDARD_PROMPT_DESCRIPTION

CURRENT_PATH_FILE = os.path.abspath(__file__)
CURRENT_PATH = os.path.dirname(CURRENT_PATH_FILE)

slash = '\\'
OS = 'Windows'
if platform.system() == 'Linux':
    OS = 'Linux'
    slash = "/"  # path of the sql Queries folder
    load_dotenv(dotenv_path=f'{CURRENT_PATH}{slash}..{slash}.env')
else:
    load_dotenv(dotenv_path=f'{CURRENT_PATH}{slash}..{slash}..{slash}.env')
    print(f"{CURRENT_PATH}..{slash}.env")


class GenerateShortScript(object):

    """
    Object to generate random scripts using openai
    """

    def __init__(self, category : str, prompt: str | None = None, model: str | None = None):

        self.standard_prompt = STANDARD_PROMPT.format(category=category)
        self.standard_model = STANDARD_MODEL

        if prompt is not None:
            self.standard_prompt = prompt

        if model:
            self.standard_model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


    def generate_script(self) -> dict:

        try:
            response_script = self.client.responses.create(
                model= self.standard_model,  # sau "gpt-4o-mini" pentru cost mai mic
                input=self.standard_prompt,
                temperature=0.9,
                max_output_tokens=80  # suficient pentru ~80 cuvinte
            )

            script = response_script.output[0].content[0].text

            response_title = self.client.responses.create(
                model=self.standard_model,  # sau "gpt-4o-mini" pentru cost mai mic
                input=STANDARD_PROMPT_TITLE.format(script=script),
                temperature=0.9,
                max_output_tokens=80  # suficient pentru ~80 cuvinte
            )

            response_description = self.client.responses.create(
                model=self.standard_model,  # sau "gpt-4o-mini" pentru cost mai mic
                input=STANDARD_PROMPT_DESCRIPTION.format(script=script),
                temperature=0.9,
                max_output_tokens=80  # suficient pentru ~80 cuvinte
            )

            title = response_title.output[0].content[0].text
            description = response_description.output[0].content[0].text

            return {
                "script" : script,
                "title" : title,
                "description" : description,
            }

        except Exception as error:

            return {
                "error" : f"Exception: {str(error)} [object] GenerateShortScript [method] generate_script()"
            }