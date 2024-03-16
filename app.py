from flask import Flask, render_template, request, jsonify

# Custom modules
import google_handlers
import gemini
import base64
import io


app = Flask(__name__)


@app.route('/')
def index():

    return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP)


@app.route('/celeb', methods=["POST"])
def celeb():

    celebrity = request.form.get("name")
    say_what = request.form.get("say")
    target_language = request.form.get("language")
    print(f"Input: {celebrity}, {say_what}, {target_language}")

    response_text, audio_path = gemini.handler(
        celebrity, say_what, model_parameters={}, target_language=target_language, audio_path="./static/audio/response.mp3")
    print(f"Response: {response_text}, {audio_path}")

    # Convert the audio to base64
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    result = {
        "response": response_text,
        "audio_base64": audio_base64
    }

    return render_template("index.html", LANG_MAP=google_handlers.LANG_MAP, result=result)


if __name__ == "__main__":
    app.run(debug=True)
