import requests


def download_image(image_url, save_path='image-output.jpg'):

    response = requests.get(image_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print('✅ Download Completed')


def image_request_handler(prompt, width, height, seed, model, save_path='image-output.jpg'):
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
