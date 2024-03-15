import google_handlers
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def get_response(prompt, generation_config=None):
    """Get a response from the model for the given prompt.

    Args
    ----
    - `prompt`: Prompt for the model.
    - `generation_config`: GenerationConfig object for the model.

    Returns
    -------
    - `str`: Response from the model.
    """

    response = model.generate_content(
        contents=prompt, generation_config=generation_config)
    return response.text


def get_config(temperature=0.9, top_k=32, top_p=1.0):
    """Returns the generation config object for the model.

    Args
    ----
    - `temperature`: Randomness of the output. High -> diverse & creative, Low -> focused & accurate.
        - Range: 0.0 to 1.0
        - Default: 0.9
    - `top_k`: Top k tokens to consider at each step. Higher -> more diverse, Lower -> more focused.
        - Range: 1 to 40
        - Default: 32
    - `top_p`: Nucleus sampling. Higher -> more diverse, Lower -> more focused.
        - Range: 0.0 to 1.0
        - Default: 1.0

    Returns
    -------
    - GenerationConfig object
    """

    return genai.GenerationConfig(
        temperature=temperature,
        top_k=top_k,
        top_p=top_p
    )


def handler(celebrity, say_what, model_parameters, target_language, audio_path):
    """
    1. Attach a pretext to the prompt (description of the website and task)
    2. Get config object using the model parameters dictionary
    3. Get response from the model
    4. Translate the response to the target_language & generate audio
    5. Return the response text & audio path

    Args
    ----
    - `celebrity`: Name of the celebrity.
    - `say_what`: What the celebrity should say.
    - `model_parameters`: Dictionary containing the model parameters.
    - `target_language`: Language to translate the response to.
    - `audio_path`: Path to save the audio file.
    """

    pretext = "You are working on a celebrity mimicking website. You need to generate text that very closely resembles the style, thought process, and humor of a celebrity. The text should be funny, engaging, deep, and thought-provoking."

    prompt = f"""{pretext}

Celebrity: {celebrity}
I want them to say: {say_what}
"""

    generation_config = get_config(
        temperature=model_parameters.get("temperature", 0.9),
        top_k=model_parameters.get("top_k", 32),
        top_p=model_parameters.get("top_p", 1.0)
    )

    response = get_response(prompt, generation_config)

    translated_response = google_handlers.translate_message(
        response, target_language)

    audio_path = google_handlers.make_audio(
        translated_response, target_language, audio_path)

    return response, audio_path


if __name__ == "__main__":

    def test_handler():

        celebrity = "Marcus Aurelius"
        say_what = "thoughts on the present day Gen-Z culture and the modern world."

        model_parameters = {"temperature": 0.9,
                            "top_k": 32,
                            "top_p": 1.0}
        target_language = "Marathi"
        audio_path = "./static/audio/marcus_aurelius.mp3"

        response, audio_path = handler(
            celebrity, say_what, model_parameters, target_language, audio_path)

        # Save input details and output in a markdown file
        with open("output.md", "w") as file:
            file.write("# Trying Gemini\n\n")
            file.write("## Input Details\n\n")
            file.write(f"- Celebrity: {celebrity}\n")
            file.write(f"- Say What: {say_what}\n")
            file.write(f"- Model Parameters: {model_parameters}\n")
            file.write(f"- Target Language: {target_language}\n")
            file.write(f"- Audio Path: {audio_path}\n\n")
            file.write("## Output\n\n")
            file.write(f"Response: {response}\n")
            file.write(f"Audio Path: {audio_path}\n")

    test_handler()
