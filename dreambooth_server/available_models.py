class AvailableModel:
    def __init__(self, name, instance_name, path_to_weights):
        self.name = name
        self.instance_name = instance_name
        self.path_to_weights = path_to_weights

MUG_MODEL = AvailableModel("mug", "zwm mug", "../stable-diffusion-weights/zwm/800")
CLOCK_MODEL = AvailableModel("clock", "zwc clock", "../stable-diffusion-weights/zwc/800")
PIZZA_MODEL = AvailableModel("pizza", "pepperoni pizza", "../stable-diffusion-weights/pepperoni-pizza/800")
COKE_MODEL = AvailableModel("bottle", "coke soda bottle", "../stable-diffusion-weights/coke/800")