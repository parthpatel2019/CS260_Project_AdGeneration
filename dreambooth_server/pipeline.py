from natsort import natsorted
from glob import glob
import os
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DDIMScheduler
from IPython.display import display

class DreamboothModel():
    def __init__(self,product_dir):
        self.product_dir = product_dir
        self.pipe = None

    def get_stable_diffusion_pipe(self):
        # Create pipeline
        model_path = natsorted(glob(self.product_dir + os.sep + "*"))[-1] # get most recent directory in product_dir
        scheduler = DDIMScheduler(beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear", clip_sample=False, set_alpha_to_one=False)
        self.pipe = StableDiffusionPipeline.from_pretrained(model_path, scheduler=scheduler, safety_checker=None, torch_dtype=torch.float16).to("cuda")
    
    def run_inference(self,prompt="zwc clock in the forest",seed=None):
        num_samples = 1 
        num_inference_steps = 100 

        # More Parameters
        negative_prompt = ""
        guidance_scale = 7.5 
        height = 512
        width = 512

        # Set cuda seed if provided
        g_cuda = torch.Generator(device='cuda')
        if seed != None:
            g_cuda.manual_seed(seed)

        # Generate Images
        with autocast("cuda"), torch.inference_mode():
            images = self.pipe(
                prompt,
                height=height,
                width=width,
                negative_prompt=negative_prompt,
                num_images_per_prompt=num_samples,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=g_cuda
            ).images
        
        return images