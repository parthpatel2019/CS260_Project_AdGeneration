import requests
import io
from config import DREAMBOOTH_API_URL
from PIL import Image

def run_dreambooth(query):
    # Returns a PIL image
    # Will take a few seconds
    params = {'query':query}
    response = requests.get(url = DREAMBOOTH_API_URL, params = params)
    image = Image.open(io.BytesIO(response.content))
    return image

def test_run_dreambooth():
    image = run_dreambooth("a zwc clock on the beach")
    image.show()