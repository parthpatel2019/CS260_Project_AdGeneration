from data_collection import DataCollection

def main():
    data_collector = DataCollection()
    image_list, words_list = data_collector.run('Chipotle_Mexican_Grill')
    if image_list is None or words_list is None:
        return 1

main()