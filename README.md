# PolyPersona

The PolyPersona project is a web application designed for generating text responses in the style of different celebrities. It utilizes natural language processing (NLP) models to mimic the speech patterns, humor, and thought processes of various public figures. Users can input the name of a celebrity, specify what they want them to say, choose a target language, and adjust model parameters to customize the response.

## Features

- **Text Generation**: Users can input a celebrity's name and specify what they want them to say. The application generates text responses that closely resemble the style of the chosen celebrity.
- **Multi-Language Support**: The application supports translation of generated text into multiple languages, enabling users to interact with the system in their preferred language.
- **Customizable Model Parameters**: Users can adjust model parameters such as `temperature`, `top-k`, and `top-p` to control the randomness and diversity of the generated text.
- **Audio Generation**: In addition to text responses, the application generates audio files corresponding to the translated text, allowing users to hear the responses in their chosen language.
- **Web Interface**: PolyPersona provides a user-friendly web interface where users can easily input their preferences and receive generated responses.

## Tech Stack

- **Flask**: Flask is used as the web framework for handling HTTP requests and rendering HTML templates.
- **gTTs**: The gTTs library is used for converting text to speech, allowing the application to generate audio files corresponding to the translated text.
- **googletrans**: The googletrans library is used for translating text into different languages, enabling users to interact with the system in their preferred language.
- **HTML/CSS/JavaScript**: Frontend components are implemented using HTML for structure, CSS for styling, and JavaScript for interactivity.
- **Python**: Python is the primary programming language used for backend development, including text generation and interaction with external APIs.
- **dotenv**: The dotenv library is used for loading environment variables from a `.env` file, providing configuration options for the application.

## How to Contribute

1. Clone the repo

   **Method 1: (Recommended)**

   - In VSCode, press `Ctrl+Shift+P`
   - Type `Git: Clone`
   - Paste the following URL: https://github.com/Hardvan/PolyPersona

   **Method 2: (Alternative)**

   Open a terminal and type the following commands:

   ```bash
   git clone https://github.com/Hardvan/FaceCounter
   cd PolyPersona
   ```

2. Create a virtual python environment by typing the following in the terminal

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment

   Windows:

   ```bash
   .\.venv\Scripts\activate
   ```

   Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies by typing the following in the terminal

   ```bash
   pip install -r requirements.txt
   ```

5. Create a google gemini API key from [here](https://ai.google.dev/)

   Create a `.env` file in the root directory of this project and add the following line:

   ```bash
   GOOGLE_API_KEY=your_api_key
   ```

   Replace `your_api_key` with the API key you got from the google gemini website.

   Warning: Don't enclose the API key in double or single quotes in the `.env` file.

   Note: Don't share your API key with anyone.

6. Run the app

   ```bash
   python app.py
   ```

7. Click on the link in the terminal to open the website

   It will look something like this:

   ```bash
   Running on http://127.0.0.1:5000
   ```
