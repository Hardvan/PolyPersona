import google_handlers
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Call ListModels to get the list of models
# all_models = genai.list_models()
# print(f"All Google AI models: {list(all_models)}")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def get_response(prompt, generation_config=None):
    """Get a response text from the model for the given prompt.

    Args
    ----
    - `prompt`: Prompt for the model.
    - `generation_config`: GenerationConfig object for the model.

    Returns
    -------
    - `str`: Response text from the model.
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


def preprocess(text):
    """Preprocess the text to remove any unwanted characters that can cause issues.
    Keep only alphanumeric characters, spaces, and punctuation.

    Args
    ----
    - `text`: Text to be preprocessed.

    Returns
    -------
    - `str`: Preprocessed text.
    """

    return ''.join(ch for ch in text if ch.isalnum() or ch.isspace() or ch in [',', '.', '!', '?', ':', ';', '-', '(', ')', '"', "'"])


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

    Returns
    -------
    - `str`: Translated response text.
    - `str`: Path to the audio file.
    """

    # Structure the prompt
    prompt = f"""You are working on a celebrity mimicking website. You need to generate text that very closely resembles the style, thought process, and humor of a celebrity. The text should be funny, engaging, deep, and thought-provoking. The response text should be plain text and keep it under 200 words.

Celebrity: {celebrity}
I want them to say: {say_what}
"""
    print(f"⌨️  Prompt:\n{prompt}")

    # Generate config object
    generation_config = get_config(
        temperature=model_parameters.get("temperature", 0.9),
        top_k=model_parameters.get("top_k", 32),
        top_p=model_parameters.get("top_p", 1.0)
    )

    # Get response from gemini model
    response = get_response(prompt, generation_config)
    response = preprocess(response)

    # Get translation & audio
    translation = google_handlers.translate_message(response, target_language)
    audio_path = google_handlers.make_audio(
        translation, target_language, audio_path)

    return translation, audio_path


def fine_tune(text, fine_tune, original_lang):
    """Fine-tune the model with the given text.

    Args
    ----
    - `text`: Text to fine-tune the model.
    - `fine_tune`: Fine-tune value. Can be "Funny", "More detailed", etc.

    Returns
    -------
    - `str`: Fine-tuned response text.
    """

    # Structure the prompt
    prompt = f"""Fine tune the following text to make it: '{fine_tune}'
    
Input text:
{text}
"""
    print(f"⌨️  Prompt:\n{prompt}")

    # Return response from gemini model
    return preprocess(get_response(prompt))


if __name__ == "__main__":

    def test_handler():

        celebrity = "Marcus Aurelius"
        say_what = "Thoughts on the modern world & Gen Z"
        model_parameters = {
            "temperature": 0.9,
            "top_k": 32,
            "top_p": 1.0
        }
        target_languages = ["Marathi", "Hindi", "Japanese", "Gujarati"]
        audio_paths = [
            "./static/audio/marcus_aurelius_marathi.mp3",
            "./static/audio/marcus_aurelius_hindi.mp3",
            "./static/audio/marcus_aurelius_japanese.mp3",
            "./static/audio/marcus_aurelius_gujarati.mp3"
        ]

        for target_language, audio_path in zip(target_languages, audio_paths):
            response, audio_path = handler(
                celebrity, say_what, model_parameters, target_language, audio_path)
            print(f"Response ({target_language}): {response}")
            print(f"Audio path ({target_language}): {audio_path}")

            # Save to markdown file
            with open(f"response_{target_language}.md", "w", encoding="utf-8") as f:
                f.write(f"# Trying gemini model\n\n")
                f.write(f"## Input\n\n")
                f.write(f"- **Celebrity**: {celebrity}\n")
                f.write(f"- **Say what**: {say_what}\n")
                f.write(f"- **Model parameters**: {model_parameters}\n")
                f.write(f"- **Target language**: {target_language}\n")
                f.write(f"- **Audio path**: {audio_path}\n\n")
                f.write(f"## Response\n\n")
                f.write(f"{response}\n\n")
                f.write(f"## Audio path\n\n")
                f.write(f"[Audio file]({audio_path})\n\n")
            print(f"Saved to response_{target_language}.md")

    test_handler()
