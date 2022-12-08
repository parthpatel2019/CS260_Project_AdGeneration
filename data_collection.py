from urllib import request
import simple_image_download.simple_image_download as downloader
import wikipedia
import string
import nltk
import shutil
import os
import requests
import json
import random
from nltk.corpus import wordnet as wn

with open("nouns.json", 'r') as f:
    nouns = json.load(f)

class DataCollection:
    def __init__(self):
        self.output_directory = './dataset/'
        self.limit = 5
        nltk.download('punkt')
        nltk.download('stopwords')
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

    def get_triggered_words(self, word):
        response_data = requests.get(f"https://api.datamuse.com/words?rel_trg={word}").json()
        words = [metadata['word'] for metadata in response_data]
        return words

    def find_nouns(self, words):
        return [word for word in words if word in nouns]

    def get_adjectives(self, word):
        response_data = requests.get(f"https://api.datamuse.com/words?rel_jjb={word}").json()
        words = [metadata['word'] for metadata in response_data]
        return words

    def get_words(self, input, num_nouns=100, num_adj=20):
        noun_adj_dict = {}

        noun_idxs = random.sample(range(len(nouns)), num_nouns)
        for i in noun_idxs:
            adj = self.get_adjectives(nouns[i])
            if len(adj) < num_adj:
                continue
            adj_idxs = random.sample(range(len(adj)), num_adj)
            adj = [adj[j] for j in adj_idxs]
            noun_adj_dict[nouns[i]] = adj

        # words = input.split(' ')

        # for word in words:
        #     triggered_words = self.get_triggered_words(word)[:10]
        #     triggered_nouns = self.find_nouns(triggered_words)
        #     for noun in triggered_nouns:
        #         adjectives =self.get_adjectives(noun)[:10]
        #         noun_adj_dict[noun] = adjectives

        '''
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
        '''

        return noun_adj_dict

    def run(self, input):
        words_dict = self.get_words(input)
        if(words_dict is None):
            return None, None
        self.remove_existing_directory(input)
        self.download_image(input)
        image_paths = []
        for i in self.my_downloader.cached_urls.keys():
            image_paths.append(str(self.my_downloader.cached_urls[i][0] + '/' + i))
        return image_paths, words_dict
