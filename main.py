from email.mime import image
from data_collection import DataCollection
from selection_model.input_generator import InputGenerator
from dreambooth import run_dreambooth

def main():
    '''    data_collector = DataCollection()
    image_list, words_list = data_collector.run('chipotle mexican grill')
    
    print(words_list)
    
    ig = InputGenerator('chipotle mexican grill')
    #print(ig.words_dict)
    prompts = ig.generate_inputs(6, 3)
    
    '''

    img = run_dreambooth('starbucks hot coffee mug')
    img.show()

    #if(image_list is None or words_list is None):
    #    return 1
    


if __name__ == '__main__':
    main()