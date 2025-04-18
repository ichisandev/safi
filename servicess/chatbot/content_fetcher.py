import httpx
import base64


def get_image_base64(image_url):
    image = httpx.get(image_url)
    image_data = base64.b64encode(image.content).decode("utf-8")
    return image_data
