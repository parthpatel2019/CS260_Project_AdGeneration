# Selection Model

## Stages:
1. Train the Score Prediction Model
    - use this round's AB test results as training data
    - use previous rounds' AB test results as validation data
2. Perform Input Selection

## Score Prediction Model (3 options):
Given input phrases and/or the generated ad creative, predict the AB test score of the creative
- Text based
    - input: one hot vector for phrases (used to generate ad creative)
    - output: score (percent)
    - architecture: fully connected NN
- Image based
    - input: ad creative image
    - output: score (percent)
    - architecture: CNN
- Ensemble
    - weighted average of both model outputs

## Input Selection:
Choose hyperparameters `N`, `S`:
- `N`: population subset size (for efficiency/randomness)
- `S`: # of creatives to use in AB test

Selection Algorithm:
1. Randomly sample `N` unseen phrase combinations
2. Predict scores for `N` samples using trained score prediction model
3. Choose `S` samples with highest predicted scores
4. Use selected samples for next AB test
