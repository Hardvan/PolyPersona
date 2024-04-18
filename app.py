from flask import Flask, render_template, request, jsonify
import base64
import os

# Custom modules
import google_handlers
import gemini


app = Flask(__name__)


# Sample Celebrities
SAMPLE_CELEBS = {
    "Marcus Aurelius": {
        "say": "Thoughts on Social Media & Gen-Z",
        "image_src": "./static/images/cards/marcus_aurelius.png"
    },
    "Buddha": {
        "say": "Entrepreneurship & Correlation with Mental Health",
        "image_src": "./static/images/cards/buddha.jpg"
    },
    "Albert Einstein": {
        "say": "Existentialism in the Digital Age",
        "image_src": "./static/images/cards/einstein.jpg"
    },
    "Chanakya": {
        "say": "48 Laws of Power & his interpretation of it",
        "image_src": "./static/images/cards/chanakya.jpg"
    },
    "Goku": {
        "say": "The importance of training & discipline",
        "image_src": "./static/images/cards/goku.jpg"
    },
}


@app.route('/')
def index():
    return render_template("index.html",
                           LANG_MAP=google_handlers.LANG_MAP,
                           SAMPLE_CELEBS=SAMPLE_CELEBS)


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

    # Check if all fields are filled
    if not celebrity or not say_what:
        return render_template("index.html",
                               LANG_MAP=google_handlers.LANG_MAP,
                               SAMPLE_CELEBS=SAMPLE_CELEBS,
                               error="Please fill in all the fields.")

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
        "celeb": celebrity,
        "say_what": say_what,
        "target_language": target_language,
        "temperature": model_parameters["temperature"],
        "top_k": model_parameters["top_k"],
        "top_p": model_parameters["top_p"],
        "response": response_text,
        "audio_base64": audio_base64
    }

    return render_template("index.html",
                           LANG_MAP=google_handlers.LANG_MAP,
                           SAMPLE_CELEBS=SAMPLE_CELEBS,
                           result=result)


@app.route("/translate_api", methods=["POST"])
def translate_api():

    print("=== In /translate_api ===")

    data = request.get_json()
    text = data.get("text")
    target_lang = data.get("target_lang")
    original_lang = data.get("original_lang")
    print(
        f"Input: {text}, Target language: {target_lang}, Original language: {original_lang}")

    # Get translation & audio
    translated_text = google_handlers.translate_message(
        text, target_lang, source=original_lang)
    audio_path = google_handlers.make_audio(
        translated_text, target_lang, audio_path="./static/audio/translated.mp3")

    # Convert the audio to base64
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    os.remove(audio_path)

    result = {
        "translated_text": translated_text,
        "audio_base64": audio_base64
    }

    print("✅ Result obtained.")

    return jsonify(result)


@app.route("/fine_tune_api", methods=["POST"])
def fine_tune_api():

    print("=== In /fine_tune_api ===")

    data = request.get_json()
    text = data.get("text")
    fine_tune = data.get("fine_tune")
    original_lang = data.get("original_lang")
    print(f"Input text: {text}, Fine-tune value: {fine_tune}",
          f"Original language: {original_lang}")

    # Call Gemini API to fine-tune the text
    fine_tuned_text = gemini.fine_tune(text, fine_tune, original_lang)

    # Get audio
    audio_path = google_handlers.make_audio(
        fine_tuned_text, target_language=original_lang, audio_path="./static/audio/fine_tuned.mp3")

    # Convert the audio to base64
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    os.remove(audio_path)

    result = {
        "fine_tuned_text": fine_tuned_text,
        "audio_base64": audio_base64
    }

    print("✅ Result obtained.")

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
