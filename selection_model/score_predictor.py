from typing import Dict, List
import gensim.downloader as api

MODEL = 'glove-wiki-gigaword-100'

class ScorePredictor:
    def __init__(self, topic: str) -> None:
        self.word_vectors = api.load(MODEL)

    # Computes similarity between prompt1 and prompt2
    def compute_similarity(self, prompt1: List[str], prompt2: List[str]) -> float:
        return self.word_vectors.n_similarity(prompt1, prompt2)

    # Predicts AB test score for prompt
    def predict_score(self, prompt: List[str], scores: Dict[List[str], float]) -> float:
        total = 0
        for tested_prompt, score in scores.items():
            total += self.compute_similarity(prompt, tested_prompt) * score
        return total / len(scores)
