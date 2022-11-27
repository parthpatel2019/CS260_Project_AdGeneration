from data_collection import DataCollection

def main():
    data_collector = DataCollection()
    image_list, words_list = data_collector.run('Sprite (drink)')
    if(image_list is None or words_list is None):
        return 1

main()