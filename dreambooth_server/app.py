from flask import Flask, send_file, request
from utils import serve_pil_image
import time
from PIL import Image
from settings import TEMP_IMAGE_LOCATION, RUNNING_LOCALLLY
from available_models import PIZZA_MODEL,COKE_MODEL

app = Flask(__name__)

if not RUNNING_LOCALLLY:
    from pipeline import DreamboothModel
    pizza_model = DreamboothModel(PIZZA_MODEL.path_to_weights)
    pizza_model.generate_stable_diffusion_pipe()
    # coke_model = DreamboothModel(COKE_MODEL.path_to_weights)
    # coke_model.generate_stable_diffusion_pipe()

def get_test_image():
    im = Image.open(TEMP_IMAGE_LOCATION)
    return im

def get_image_for_query(query,model):
    images = model.run_inference(query)
    return images[0]

def get_model(model_id):
    if model_id == "pizza":
        return pizza_model
    # elif model_id == 'coke':
    #     return coke_model
    else:
        raise ValueError("Invalid model_id: must be pizza or coke")

@app.route("/")
def single_image():
    query = request.args.get('query')
    model_id = request.args.get('model_id')

    # Get image dependent on where we are running
    if RUNNING_LOCALLLY:
        image = get_test_image()
    else:
        model = get_model(model_id)
        image = get_image_for_query(query,model)
    
    ret = serve_pil_image(image)
    image.close()
    return ret