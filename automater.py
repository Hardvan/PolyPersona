import FlaskStarter
import FileHarvestor

if __name__ == "__main__":
    # FlaskStarter.create_flask_project()
    FileHarvestor.read_files(["app.py", "gemini.py", "google_handlers.py"])
