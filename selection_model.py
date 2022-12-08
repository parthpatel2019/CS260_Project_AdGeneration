import nltk
from selection_model.input_generator import InputGenerator


gen = InputGenerator("pepperoni pizza")
results = gen.generate_inputs(100, 10)
for res in results:
    print(res)