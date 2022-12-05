from flask import Flask, send_file, request
from utils import serve_pil_image
import time
from PIL import Image

app = Flask(__name__)

model = None
TEMP_IMAGE_LOCATION = "test.jpeg"
RUNNING_LOCALLLY = True

def get_test_image():
    im = Image.open(TEMP_IMAGE_LOCATION)
    return im

def get_image_for_query(query):
    if RUNNING_LOCALLLY:
        return get_test_image()
    else: 
        from pipeline import DreamboothModel
        images = model.run_inference(query)
        return images[0]

@app.route("/")
def hello_world():
    query = request.args.get('query')
    image = get_image_for_query(query)
    ret = serve_pil_image(image)
    image.close()
    return ret

if not RUNNING_LOCALLLY:
    from pipeline import DreamboothModel
    model = DreamboothModel("../stable-diffusion-weights/zwc")
    model.get_stable_diffusion_pipe()