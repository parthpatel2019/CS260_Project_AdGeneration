import requests
import io
from config import DREAMBOOTH_API_URL
from PIL import Image

def run_dreambooth(query,model_id):
    # Returns a PIL image
    # Will take a few seconds

    # coke model expects 'coke soda bottle' in the query
    # pizza model expects 'pepperoni pizza' in the query
    if model_id not in ['pizza', 'coke']:
        raise ValueError("Invalid model_id")

    params = {'query':query, "model_id": model_id}
    response = requests.get(url = DREAMBOOTH_API_URL, params = params)
    image = Image.open(io.BytesIO(response.content))
    return image

def test_run_dreambooth():
    image = run_dreambooth("a pepperoni pizza on the beach", "pizza")
    image.show()