from reportlab.pdfgen import canvas


def generate_pdf(celeb, say_what, target_language, temperature, top_k, top_p, response):
    """Generates a PDF document with the provided celebrity prompt, response, and details.

    Args
    ----
    - `celeb`: The celebrity name used in the prompt.
    - `say_what`: The prompt instructing the Bard API.
    - `target_language`: The target language for the response.
    - `temperature`: Controls the randomness of the generated text.
    - `top_k`: Restricts the vocabulary used in generation.
    - `top_p`: Controls the focus of the generated text.
    - `response`: The response generated by the Bard API.

    Returns
    -------
    - `pdf_path`: The file path of the generated PDF document.
    """

    pdf_path = "./static/pdfs/generated_pdf.pdf"

    # Create a PDF document
    pdf = canvas.Canvas(pdf_path)

    # Set font and title
    pdf.setFont("Helvetica", size=14)
    pdf.drawString(30, 750, "Celebrity Quote Generation")

    # Add prompt details
    y_pos = 700
    pdf.drawString(30, y_pos, f"Celebrity: {celeb}")
    y_pos -= 20
    pdf.drawString(30, y_pos, f"Prompt: {say_what}")
    y_pos -= 20
    pdf.drawString(30, y_pos, f"Target Language: {target_language}")
    y_pos -= 20
    pdf.drawString(30, y_pos, f"Temperature: {temperature}")
    y_pos -= 20
    pdf.drawString(30, y_pos, f"Top-k: {top_k}")
    y_pos -= 20
    pdf.drawString(30, y_pos, f"Top-p: {top_p}")

    # Add response text
    y_pos -= 40  # Add some spacing
    pdf.setFont("Helvetica", size=12)
    pdf.drawString(30, y_pos, "Response:")
    pdf.drawString(50, y_pos - 10, response)

    # Save the PDF document
    pdf.save()

    # Return the file path
    return pdf_path


if __name__ == "__main__":

    # Test the `generate_pdf` function
    celeb = "Elon Musk"
    say_what = "I am going to Mars!"
    target_language = "English"
    temperature = 0.7
    top_k = 50
    top_p = 0.9
    response = "That's great! When are you planning to go?"

    pdf_path = generate_pdf(celeb, say_what, target_language,
                            temperature, top_k, top_p, response)
    print(f"PDF Path: {pdf_path}")
