from ctypes import ArgumentError
from typing import Dict, List
import numpy as np

from selection_model.score_predictor import ScorePredictor
from data_collection import DataCollection


PROMPT_MIN_SIZE = 0
PROMPT_MAX_SIZE = 3
MAX_ITER = 20

class InputGenerator:
    def __init__(self, topic: str, scores: Dict[str, float] = dict()) -> None:
        data = DataCollection(topic)
        self.topic = topic
        self.words_dict = data.get_words()
        self.phrases = data.get_phrases()
        self.scores = scores
        self.predictor = ScorePredictor(scores)

    # Select output_num best samples from a pool of sample_num random unseen samples
    def generate_inputs(self, sample_num: int, output_num: int) -> List[str]:
        if output_num < 0 or output_num > sample_num:
            print('Invalid input!')
            raise ArgumentError

        phrases = np.array(self.phrases)
        nouns = np.array(list(self.words_dict.keys()))

        tested_prompts = set(self.scores.keys())
        unseen_prompts = set()
        rng = np.random.default_rng()
        it = 0

        # Generating sample_num number of unseen prompts
        while len(unseen_prompts) < sample_num and it < MAX_ITER:
            n = sample_num - len(unseen_prompts)

            # Randomly sample phrases and nouns
            phrase_idxs = rng.integers(phrases.size, size=n)
            noun_idxs = rng.integers(nouns.size, size=(n, PROMPT_MAX_SIZE))
            num_nouns = rng.integers(low=PROMPT_MIN_SIZE, high=PROMPT_MAX_SIZE, size=n, endpoint=True)

            # Construct prompts from sampled phrases
            phrase_samples = phrases[phrase_idxs]
            noun_samples = nouns[noun_idxs]
            prompt_samples = [f"{self.topic} {phrase}" for phrase in phrase_samples]

            for i in range(n):
                sample_nouns = noun_samples[i][:num_nouns[i]]
                if sample_nouns.size > 0:
                    pairs = [f"{np.random.choice(self.words_dict[noun])} {noun}" for noun in sample_nouns]
                    prompt_samples[i] += ', ' + ', '.join(pairs)

            unseen_prompts |= set(prompt_samples) - tested_prompts
            it += 1


        # Find prompts with highest predicted scores
        prompts = np.array(list(unseen_prompts))
        pred_scores = list(map(self.predictor.predict_score, prompts))
        best_i = np.argsort(pred_scores)[-output_num:]
        best_prompts = prompts[best_i]

        return best_prompts
        