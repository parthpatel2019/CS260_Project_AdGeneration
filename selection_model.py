import nltk
from selection_model.input_generator import InputGenerator


gen = InputGenerator("pepperoni pizza")
print(gen.generate_inputs(100, 10))