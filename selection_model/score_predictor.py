from typing import Dict, List
import gensim.downloader as api

MODEL = 'glove-wiki-gigaword-100'

class ScorePredictor:
    def __init__(self, scores: Dict[str, float]) -> None:
        self.word_vectors = api.load(MODEL)
        self.scores = scores

    # Computes similarity between prompt1 and prompt2
    def compute_similarity(self, prompt1: str, prompt2: str) -> float:
        words1 = prompt1.replace(',', '').split(' ')
        words2 = prompt2.replace(',', '').split(' ')
        return self.word_vectors.n_similarity(words1, words2)

    # Predicts AB test score for prompt
    def predict_score(self, prompt: str) -> float:
        if not self.scores:
            return 0

        total = 0
        for tested_prompt, score in self.scores.items():
            total += self.compute_similarity(prompt, tested_prompt) * score
        return total / len(self.scores)

if __name__ == "__main__":
    p = ScorePredictor({})
    p1 = "pepperoni pizza cold"
    p2 = "pepperoni pizza hot cheesy"
    print(p.compute_similarity(p1, p2))