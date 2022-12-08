from email.mime import image
import json
from data_collection import DataCollection
from selection_model.input_generator import InputGenerator
from dreambooth import run_dreambooth
from ab_testing import ABTester
from PIL import Image


SPECIAL_SUFFIXES = ["Norman Rockwell style", "Starry Night Van Gogh Style", "drain Anime Style", "on the beach"]
SCORES_FILE = ''
BASE_IMG_FILE = ''


def main():
    '''    data_collector = DataCollection()
    image_list, words_list = data_collector.run('chipotle mexican grill')
    
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

    gen = InputGenerator("pizza", scores=scores, suffixes=SPECIAL_SUFFIXES)
    prompts = gen.generate_inputs(100, 10)
    prompt_img_dict = {}
    for prompt in prompts:
        img = run_dreambooth("pepperoni pizza, " + prompt, 'pizza')
        print(prompt)
        prompt_img_dict[prompt] = img
        img.show()
        tester = ABTester(base_img, img, 5)
        score = tester.run()
        gen.score[prompt] = score
        #print(img)
    
    #print(prompt_img_dict)

    #if(image_list is None or words_list is None):
    #    return 1

    if SCORES_FILE:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f)
    


if __name__ == '__main__':
    main()