import simple_image_download.simple_image_download as downloader
import wikipedia
import string
import nltk
import shutil
import os

class DataCollection:
    def __init__(self):
        self.output_directory = './dataset/'
        self.limit = 5
        nltk.download('punkt')
        self.my_downloader = downloader.Downloader()
        self.my_downloader.directory = self.output_directory
        self.my_downloader.extensions = '.jpg'

    def download_image(self, input):
        self.my_downloader.download(input, limit=self.limit)

    def remove_existing_directory(self, input):
        dir_path = self.output_directory + '/' + str(input)
        dir_exist = os.path.isdir(dir_path)
        if dir_exist:
            try:
                shutil.rmtree(dir_path)
                print("Directory deleted so continue download...")
            except:
                print("Error in Removing Directory")
        else:
            print("Directory does not exist so continue download...")

    def get_words(self, input):
        try:
            text = wikipedia.summary(input)
        except:
            print("Error: Cannot find wikipedia summary for this input.")
            print("Try something specific\nExample: Sprite -> Sprite (drink)")
            return None
        word_tokens = nltk.tokenize.word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w.lower() in list(nltk.corpus.stopwords.words('english'))]
        filtered_sentence = [w for w in filtered_sentence if not w.lower() in list(string.punctuation)]
        filtered_sentence = [w for w in filtered_sentence if not "'s" in w.lower()]
        filtered_sentence = [w for w in filtered_sentence if not any(chr.isdigit() for chr in w.lower())]
        filtered_sentence = [*set(filtered_sentence)]
        return filtered_sentence

    def run(self, input):
        words_list = self.get_words(input)
        if(words_list is None):
            return None, None
        self.remove_existing_directory(input)
        self.download_image(input)
        image_paths = []
        for i in self.my_downloader.cached_urls.keys():
            image_paths.append(str(self.my_downloader.cached_urls[i][0] + '/' + i))
        return image_paths, words_list
