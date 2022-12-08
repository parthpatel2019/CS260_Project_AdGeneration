from email.mime import image
from data_collection import DataCollection
from selection_model.input_generator import InputGenerator
from dreambooth import run_dreambooth


SPECIAL_SUFFIXES = ["Norman Rockwell style", "Starry Night Van Gogh Style", "drain Anime Style", "on the beach"]

def main():
    '''    data_collector = DataCollection()
    image_list, words_list = data_collector.run('chipotle mexican grill')
    
    print(words_list)
    
    ig = InputGenerator('chipotle mexican grill')
    #print(ig.words_dict)
    prompts = ig.generate_inputs(6, 3)
    
    '''
    gen = InputGenerator("pizza", suffixes=SPECIAL_SUFFIXES)
    prompts = gen.generate_inputs(100, 10)
    prompt_img_dict = {}
    for prompt in prompts:
        img = run_dreambooth("pepperoni pizza, " + prompt, 'pizza')
        print(prompt)
        prompt_img_dict[prompt] = img
        img.show()
        #print(img)
    
    #print(prompt_img_dict)

    #if(image_list is None or words_list is None):
    #    return 1
    


if __name__ == '__main__':
    main()