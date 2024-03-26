from flask import Flask, render_template, request, jsonify

# Custom modules
import google_handlers
import gemini
import base64
import os


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
}


@app.route('/')
def index():
    return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP, SAMPLE_CELEBS=SAMPLE_CELEBS)


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
        return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP, SAMPLE_CELEBS=SAMPLE_CELEBS, error="Please fill in all the fields.")

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

    return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP, SAMPLE_CELEBS=SAMPLE_CELEBS, result=result)


if __name__ == "__main__":
    app.run(debug=True)
