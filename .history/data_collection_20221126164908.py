from bing_image_downloader import downloader
import wikipedia
import string
import nltk
import shutil
import os

class DataCollection:
    def __init__(self):
        self.output_directory = './dataset'
        self.limit = 5
        nltk.download('punkt')

    def download_image(self, input):
        downloader.download(input, limit=self.limit,  output_dir=self.output_directory,
                            timeout=5, filter="photo", verbose=False)

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

    def get_syn(self, input):
        try:
            text = wikipedia.summary(input)
        except:
            print("Error: Cannot find wikipedia summary for this input.")
            print("Try something specific\nExample: Sprite -> Sprite (drink)")
            return None
        remove_words = list(nltk.corpus.stopwords.words('english')) + list(string.punctuation) + list(["'s"]) + list(['1','2','3','4','5','6','7','8','9','0'])
        word_tokens = nltk.tokenize.word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w.lower() in remove_words]
        return filtered_sentence

    def run(self, input):
        words_list = self.get_syn(input)
        if(words_list is None):
            return None, None
        dir_path = self.output_directory + '/' + str(input)
        image_paths = []
        self.remove_existing_directory(input)
        self.download_image(input)
        for i in range(self.limit):
            image_paths.append(dir_path + '/Image_' + str(i))
        return image_paths, words_list
