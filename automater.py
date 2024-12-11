import FlaskStarter
import FileHarvestor

if __name__ == "__main__":
    # FlaskStarter.create_flask_project()

    readme = "README.md"
    app_py = "app.py"
    gemini_py = "gemini.py"
    google_handlers_py = "google_handlers.py"
    pollinations_py = "pollinations.py"
    pdf_handler_py = "pdf_handler.py"
    index_html = "templates/index.html"
    io_html = "templates/io.html"

    FileHarvestor.read_files([app_py, index_html, io_html])
