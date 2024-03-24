# Contents

## app.py

from flask import Flask, render_template, request, jsonify

# Custom modules
import google_handlers
import gemini
import base64
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP)


@app.route('/celeb', methods=["POST"])
def celeb():

    # Fetch form data
    celebrity = request.form.get("name")
    say_what = request.form.get("say")
    target_language = request.form.get("language")
    temperature = request.form.get("temperature")
    top_k = request.form.get("top_k")
    top_p = request.form.get("top_p")
    print(f"Input: {celebrity}, {say_what}, {target_language}")
    print(
        f"Model parameters (temperature, top_k, top_p): {temperature}, {top_k}, {top_p}")

    model_parameters = {
        "temperature": float(temperature),
        "top_k": int(top_k),
        "top_p": float(top_p)
    }

    # Get the response
    response_text, audio_path = gemini.handler(celebrity, say_what,
                                               model_parameters=model_parameters,
                                               target_language=target_language,
                                               audio_path="./static/audio/response.mp3")
    print(f"Response: {response_text}, {audio_path}")

    # Convert the audio to base64
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    os.remove(audio_path)  # audio file not needed anymore (we have base64)

    result = {
        "response": response_text,
        "audio_base64": audio_base64
    }

    return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP, result=result)


if __name__ == "__main__":
    app.run(debug=True)


## gemini.py

import google_handlers
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


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
    print(f"Prompt: {prompt}")

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


## google_handlers.py

from googletrans import Translator
from gtts import gTTS
import os


# ? Language mapping
# Available languages
LANG_MAP = {"English": "en",
            "Hindi": "hi",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Kannada": "kn",
            "Tamil": "ta",
            "Telugu": "te",
            "Malayalam": "ml",
            "Bengali": "bn",
            "Japanese": "ja",
            }

# Dictionary to cache translations
TRANSLATION_CACHE = {}  # { (text, lang): translation }


def translate_message(text, lang):
    """Translate the given text to the given language. If the translation is
    already in the cache, it will not be translated again.

    Args
    ----
    - `text`: Text to be translated.
    - `lang`: Language to translate to.

    Returns
    -------
    - `str`: Translated text.
    """

    # Check if the translation is already in the cache
    cache_key = (text, lang)
    if cache_key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[cache_key]

    # Translate the text
    translator = Translator()
    translation = translator.translate(text, src="en", dest=LANG_MAP[lang])

    # Cache the translation
    TRANSLATION_CACHE[cache_key] = translation.text

    return translation.text


# Dictionary to cache audio files
AUDIO_CACHE = {}  # { (text, lang): audio_path }


def make_audio(text, lang, audio_path=None, regen=False):
    """Generate an audio file for the given text in the given language and
    save it to the specified path. If the audio file is already in the cache,
    it will not be generated again unless regen is set to True.

    Args
    ----
    - `text`: Text to be converted to audio.
    - `lang`: Language of the text.
    - `audio_path`: Path to save the audio file. Defaults to None.
                    Make sure that the folder exists (will be created automatically in future versions).
    - `regen`: If True, the audio file will be regenerated
               even if it is already in the cache. Defaults to False.

    Raises
    ------
    - `ValueError`: If audio_path is not provided.

    Returns
    -------
    - `str`: Path to the generated audio file.
    """

    if audio_path is None:
        raise ValueError("Audio path not provided.")

    # Check if the audio is already in the cache
    cache_key = (text, lang)
    if not regen and cache_key in AUDIO_CACHE and os.path.exists(AUDIO_CACHE[cache_key]):
        return AUDIO_CACHE[cache_key]

    # Generate the audio file
    tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
    tts.save(audio_path)

    # Cache the audio file
    AUDIO_CACHE[cache_key] = audio_path

    return audio_path


def display_cache():

    LINE = "====================================="

    print("\n")
    print(LINE)
    print("Cache contents")
    print(LINE)
    print("Translation cache:", TRANSLATION_CACHE)
    print("Audio cache:", AUDIO_CACHE)


if __name__ == "__main__":

    def test_translate_message():
        """Test the translate_message function.

        Output:
        =====================================
        Running time for translate_message()
        =====================================
        Text length: 1900

        Test 1: Without caching
        Time taken without caching (Test 1): 2185.41ms

        Test 2: Without caching (different request)
        Time taken without caching (Test 2): 1658.46ms

        Test 3: With caching
        Time taken with caching (Test 3): 0.00ms
        """

        import time

        LINE = "====================================="

        # Check the running time for translate_message
        print(LINE)
        print("Running time for translate_message()")
        print(LINE)
        text = "Hello, how are you?" * 100
        print("Text length:", len(text))

        # Test 1: Without caching (same translation request)
        print("\nTest 1: Without caching")
        start = time.time()
        translate_message(text, "Hindi")
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 1): {s:.2f}s")

        # Test 2: Without caching (different translation request)
        print("\nTest 2: Without caching (different request)")
        start = time.time()
        translate_message(text, "Marathi")
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 2): {s:.2f}s")

        # Test 3: With caching (same translation request)
        print("\nTest 3: With caching")
        start = time.time()
        translate_message(text, "Hindi")
        end = time.time()
        s = end - start
        print(f"Time taken with caching (Test 3): {s:.2f}s")

    def test_make_audio():
        """Test the make_audio function.

        Output:
        =====================================
        Running time for make_audio()
        =====================================
        Text length: 190

        Test 1: Without caching
        Time taken without caching (Test 1): 4388.61ms

        Test 2: Without caching (different request)
        Time taken without caching (Test 2): 4768.54ms

        Test 3: With caching
        Time taken with caching (Test 3): 0.00ms
        """

        import time

        LINE = "====================================="

        # Check the running time for make_audio
        print("\n")
        print(LINE)
        print("Running time for make_audio()")
        print(LINE)
        text = "Hello, how are you?" * 10
        print("Text length:", len(text))

        # Test 1: Without caching (same translation request)
        print("\nTest 1: Without caching")
        start = time.time()
        audio_path_1 = make_audio(
            text, "Hindi", audio_path="./static/audio/test_1.mp3")
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 1): {s:.2f}s")

        # Test 2: Without caching (different translation request)
        print("\nTest 2: Without caching (different request)")
        start = time.time()
        audio_path_2 = make_audio(
            text, "Marathi", audio_path="./static/audio/test_2.mp3")
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 2): {s:.2f}s")

        # Test 3: With caching (same translation request)
        print("\nTest 3: With caching")
        start = time.time()
        audio_path_1 = make_audio(
            text, "Hindi", audio_path=audio_path_1)
        end = time.time()
        s = end - start
        print(f"Time taken with caching (Test 3): {s:.2f}s")

        # Delete the audio files
        os.remove(audio_path_1)
        os.remove(audio_path_2)

    test_translate_message()
    test_make_audio()
    # display_cache()


