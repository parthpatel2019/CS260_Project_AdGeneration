from typing import Dict, List
import numpy as np

from score_predictor import ScorePredictor
from ..data_collection import DataCollection

PROMPT_MIN_SIZE = 4
PROMPT_MAX_SIZE = 16

class InputGenerator:
    def __init__(self, topic: str, scores: Dict[List[str], float]) -> None:
        data = DataCollection()
        self.words = data.get_words(topic)
        self.scores = scores
        self.predictor = ScorePredictor(topic)

    # Select output_num best samples from a pool of sample_num random unseen samples
    def generate_inputs(self, sample_num: int, output_num: int) -> List[List[str]]:
        if output_num < 0 or output_num > sample_num:
            pass

        words = np.array(self.words)
        tested_prompts = set(map(np.array, self.scores.keys()))
        unseen_prompts = set()
        rng = np.random.default_rng()

        # Generating sample_num number of unseen prompts
        # Currently fixed length prompt, variable length may be better if time
        while len(unseen_prompts) < sample_num:
            n = sample_num - len(unseen_prompts)
            num_samples = rng.integers(low=0, high=len(self.words), size=(n, PROMPT_MAX_SIZE))
            word_samples = words[num_samples]
            unseen_i = [i for i, prompt in enumerate(word_samples) if prompt not in tested_prompts]

        # Find prompts with highest scores
        unseen_prompts = list(unseen_prompts)
        pred_scores = np.zeros(len(unseen_prompts))
        for i, prompt in enumerate(unseen_prompts):
            pred_scores[i] = self.predictor.predict_score(prompt, self.scores)

        best_i = np.argsort(pred_scores)[-output_num:]
        return unseen_prompts[best_i]
        

        