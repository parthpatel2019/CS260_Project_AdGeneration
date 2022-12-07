from flask import Flask, send_file, request
from utils import serve_pil_image
import time
from PIL import Image
from settings import TEMP_IMAGE_LOCATION, RUNNING_LOCALLLY

app = Flask(__name__)

model = None

if not RUNNING_LOCALLLY:
    from pipeline import DreamboothModel
    model = DreamboothModel("../stable-diffusion-weights/zwc")
    model.generate_stable_diffusion_pipe()

def get_test_image():
    im = Image.open(TEMP_IMAGE_LOCATION)
    return im

def get_image_for_query(query):
    from pipeline import DreamboothModel
    images = model.run_inference(query)
    return images[0]

@app.route("/")
def single_image():
    query = request.args.get('query')

    # Get image dependent on where we are running
    if RUNNING_LOCALLLY:
        image = get_test_image()
    else:
        image = get_image_for_query(query)
    
    ret = serve_pil_image(image)
    image.close()
    return ret