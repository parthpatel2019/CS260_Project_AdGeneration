from email.mime import image
import json
from data_collection import DataCollection
from selection_model.input_generator import InputGenerator
from dreambooth import run_dreambooth
from ab_testing import ABTester
from PIL import Image


SCORES_FILE = 'scores.json'
BASE_IMG_FILE = 'base_img.jpeg'


def main():
    '''    data_collector = DataCollection('chipotle mexican grill')
    image_list, words_list = data_collector.run()
    
    print(words_list)
    
    ig = InputGenerator('chipotle mexican grill')
    #print(ig.words_dict)
    prompts = ig.generate_inputs(6, 3)
    
    '''
    scores = {}
    if SCORES_FILE:
        with open(SCORES_FILE, 'r') as f:
            scores = json.load(f)

    base_img = Image.open(BASE_IMG_FILE)

    gen = InputGenerator("pepperoni pizza", scores=scores)
    prompts = gen.generate_inputs(100, 10)
    prompt_img_dict = {}
    for prompt in prompts:
        img = run_dreambooth(prompt, 'pizza')
        print(prompt)
        prompt_img_dict[prompt] = img
        img.show()
        tester = ABTester(base_img, img, 5)
        score = tester.run()
        scores[prompt] = score
        #print(img)
    
    #print(prompt_img_dict)

    #if(image_list is None or words_list is None):
    #    return 1

    if SCORES_FILE:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f)
    


if __name__ == '__main__':
    main()