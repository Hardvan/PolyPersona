import requests


def download_image(image_url, save_path='image-output.jpg'):
    """Download the image from the given URL and save it to the specified path.

    Args
    ----
    - `image_url`: URL of the image to download.
    - `save_path`: Path to save the image. Defaults to 'image-output.jpg'.
    """

    response = requests.get(image_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print('✅ Download Completed')


def image_request_handler(prompt, width, height, seed, model, save_path='image-output.jpg'):
    """Generates an image based on the given prompt and saves it to the specified path.

    Args
    ----
    - `prompt`: The prompt for the image generation.
    - `width`: Width of the generated image.
    - `height`: Height of the generated image.
    - `seed`: Seed value for the image generation.
    - `model`: Model to use for image generation.
    - `save_path`: Path to save the generated image. Defaults to 'image-output.jpg'.

    Returns
    -------
    - `str`: Path to the saved image.
    """

    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    download_image(image_url, save_path)
    return save_path


if __name__ == "__main__":

    # Image details
    prompt = 'Create a detailed illustration of a magnificent Indian tiger in a jungle setting.'
    width = 1024
    height = 1024
    seed = 42
    model = 'flux'

    image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"

    download_image(image_url)
