from ctypes import ArgumentError
from typing import Dict, List
import numpy as np

from selection_model.score_predictor import ScorePredictor
from data_collection import DataCollection
from keytotext import pipeline
 
# Load the base pre-trained T5 model
# It will download three files: 1. config.json, 2. tokenizer.json, 3. pytorch_model.bin (~850 MB)
#nlp = pipeline("k2t-base")

PROMPT_MIN_SIZE = 1
PROMPT_MAX_SIZE = 7


class InputGenerator:
    def __init__(self, topic: str, scores: Dict[List[str], float] = dict(), suffixes: List[str] = list()) -> None:
        data = DataCollection()
        self.topic = topic
        self.words_dict = data.get_words(topic)
        self.scores = scores
        self.predictor = ScorePredictor()
        self.suffixes = suffixes

    # Select output_num best samples from a pool of sample_num random unseen samples
    def generate_inputs(self, sample_num: int, output_num: int) -> List[str]:
        if output_num < 0 or output_num > sample_num:
            print('Invalid input!')
            raise ArgumentError

        tested_prompts = set(map(np.array, self.scores.keys())) 
        unseen_prompts = set()
        rng = np.random.default_rng()

        # Generating sample_num number of unseen prompts
        # Currently fixed length prompt, variable length may be better if time
        while len(unseen_prompts) < sample_num:
            n = sample_num - len(unseen_prompts)
            nouns = np.array(list(self.words_dict.keys()))
            num_samples = rng.integers(low=0, high=len(self.words_dict), size=(n, PROMPT_MAX_SIZE))
            sample_sizes = rng.integers(low=PROMPT_MIN_SIZE, high=PROMPT_MAX_SIZE+1, size=n)
            
            noun_samples = nouns[num_samples]
            pair = lambda noun: (np.random.choice(self.words_dict[noun]), noun)
            noun_adj_pairs = [tuple([pair(nouns[j]) for j in range(sample_sizes[i])]) for i, nouns in enumerate(noun_samples)]
            
            # Configure the model parameters
            #config = {"do_sample": True, "num_beams": 4, "no_repeat_ngram_size": 3, "early_stopping": True}
            
            # Provide list of keywords into the model as input
            #sentences = np.array([nlp(word_vec, **config) for word_vec in word_samples])

            unseen_i = [i for i, prompt in enumerate(noun_adj_pairs) if set(prompt) not in tested_prompts]
            unseen_prompts = np.array(noun_adj_pairs, dtype=np.object)[unseen_i]


        # Find prompts with highest scores
        pred_scores = np.zeros(len(unseen_prompts))
        for i, prompt in enumerate(unseen_prompts):
            pred_scores[i] = self.predictor.predict_score(prompt, self.scores)

        best_i = np.argsort(pred_scores)[-output_num:]
        best_prompts = unseen_prompts[best_i]

        # Convert to string prompts
        output = list(map(lambda x: ', '.join([' '.join(y) for y in x]), best_prompts))
        output = [f"{self.topic}, {prompt}" for prompt in output]
        output = [f"{prompt}, {suffix}" for prompt in output for suffix in self.suffixes]

        return output
        