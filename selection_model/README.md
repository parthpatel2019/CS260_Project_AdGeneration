# Selection Model

## Stages
1. Train the Score Prediction Model
2. Perform Input Selection

## Stage 1: Score Prediction Model
Given input prompts and/or the generated ad creative, predict the AB test score of the creative

### Phase A: Pre-Trained Model
This is our initial approach that should work better with limited time/resources.

1. Encode tested prompts as word2vec embeddings using `gensim`
    - https://radimrehurek.com/gensim/
2. [Define similarity metric between two prompts] 
    - range: [0, 1]
    - some form of cosine similarity
3. Given untested prompt, compute similarity to all tested prompts
4. Use weighted average of similarities as predicted score
    - using AB test scores for weights

### Phase B: Custom Model (3 options)
This would be a nice-to-have given sufficient time/resources. Could be part of "Future Works" section in the report.

- Text based
    - input: one hot vector for prompts (used to generate ad creative)
    - output: score (percent)
    - architecture: fully connected NN
- Image based
    - input: ad creative image
    - output: score (percent)
    - architecture: CNN
- Ensemble
    - weighted average of both model outputs

#### Data Split
- use this round's AB test results as training data
- use previous rounds' AB test results as validation data

## Stage 2: Input Selection
Choose hyperparameters `N`, `S`:
- `N`: population subset size (for efficiency/randomness)
- `S`: # of creatives to use in AB test

Selection Algorithm:
1. Randomly sample `N` unseen prompts
2. Predict scores for `N` prompts using score prediction model
3. Choose `S` prompts with highest predicted scores
4. Use selected prompts for next AB test
