import nltk
from selection_model.input_generator import InputGenerator

topic = "pepperoni pizza"
gen = InputGenerator(topic, {f"{topic} on the beach": 1.0})
results = gen.generate_inputs(100, 10)
for res in results:
    print(res)