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


def translate_message(text, lang, use_cache=False):
    """Translate the given text to the given language. If the translation is
    already in the cache, it will not be translated again.

    Args
    ----
    - `text`: Text to be translated.
    - `lang`: Language to translate to.
    - `use_cache`: If True, the translation will be fetched from the cache
                     if it is available. Defaults to False.

    Returns
    -------
    - `str`: Translated text.
    """

    # Check if the translation is already in the cache
    if use_cache:
        cache_key = (text, lang)
        if cache_key in TRANSLATION_CACHE:
            return TRANSLATION_CACHE[cache_key]

    # Translate the text
    translator = Translator()
    translation = translator.translate(text, src="en", dest=LANG_MAP[lang])

    # Cache the translation
    if use_cache:
        TRANSLATION_CACHE[cache_key] = translation.text

    return translation.text


# Dictionary to cache audio files
AUDIO_CACHE = {}  # { (text, lang): audio_path }


def make_audio(text, lang, audio_path=None, regen=False, use_cache=False):
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
    - `use_cache`: If True, the audio file will be fetched from the cache
                   if it is available. Defaults to False.

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
    if use_cache:
        cache_key = (text, lang)
        if not regen and cache_key in AUDIO_CACHE and os.path.exists(AUDIO_CACHE[cache_key]):
            return AUDIO_CACHE[cache_key]

    # Generate the audio file
    tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
    tts.save(audio_path)

    # Cache the audio file
    if use_cache:
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
        translate_message(text, "Hindi", use_cache=True)
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 1): {s:.2f}s")

        # Test 2: Without caching (different translation request)
        print("\nTest 2: Without caching (different request)")
        start = time.time()
        translate_message(text, "Marathi", use_cache=True)
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 2): {s:.2f}s")

        # Test 3: With caching (same translation request)
        print("\nTest 3: With caching")
        start = time.time()
        translate_message(text, "Hindi", use_cache=True)
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
            text, "Hindi", audio_path="./static/audio/test_1.mp3", use_cache=True)
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 1): {s:.2f}s")

        # Test 2: Without caching (different translation request)
        print("\nTest 2: Without caching (different request)")
        start = time.time()
        audio_path_2 = make_audio(
            text, "Marathi", audio_path="./static/audio/test_2.mp3", use_cache=True)
        end = time.time()
        s = end - start
        print(f"Time taken without caching (Test 2): {s:.2f}s")

        # Test 3: With caching (same translation request)
        print("\nTest 3: With caching")
        start = time.time()
        audio_path_1 = make_audio(
            text, "Hindi", audio_path=audio_path_1, use_cache=True)
        end = time.time()
        s = end - start
        print(f"Time taken with caching (Test 3): {s:.2f}s")

        # Delete the audio files
        os.remove(audio_path_1)
        os.remove(audio_path_2)

    test_translate_message()
    test_make_audio()
    # display_cache()
