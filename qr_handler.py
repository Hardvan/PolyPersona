import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps


def save_qr_code(url, path="./static/qr/qr.png"):
    """Generates a QR code by embedding the given url and saves it to the given path.

    Args:
    - `url`: The URL to embed in the QR code.
    - `path`: The path to save the QR code.

    Returns:
    - str: The path to the saved QR code.
    """

    # Create the folder if it doesn't exist
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create image with caption
    img_with_caption = Image.new(
        'RGB', (qr_img.size[0], qr_img.size[1] + 50), color='white')
    img_with_caption.paste(qr_img, (0, 20))  # Move QR code down by 20 pixels

    # Add caption text
    draw = ImageDraw.Draw(img_with_caption)
    font_path = "./static/fonts/Roboto-Regular.ttf"
    font_size = 15
    font = ImageFont.truetype(font_path, font_size)
    caption = "Scan the above QR code to access the website."
    text_width = draw.textlength(caption, font)
    draw.text(((qr_img.size[0] - text_width) / 2, qr_img.size[1] + 10),
              caption, fill="black", font=font)

    # Add borders with spacing
    border_width = 3
    spacing = 10
    img_with_borders = ImageOps.expand(
        img_with_caption, border=border_width, fill='blue')
    img_with_borders = ImageOps.expand(
        img_with_borders, border=spacing, fill='white')

    # Offset the employee logo by 5 pixels from the top
    logo_path = "./static/logo/cust_logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50))  # Adjust the size as needed
        img_with_borders.paste(
            logo, ((img_with_borders.width - logo.width) // 2, spacing + 7))
    else:
        raise FileNotFoundError(f"Logo not found at {logo_path}")

    # Save image
    img_with_borders.save(path)
    print(f"✅ Saved QR code to: {path}")

    return path


if __name__ == "__main__":

    url = "https://www.google.com"
    save_qr_code(url)
