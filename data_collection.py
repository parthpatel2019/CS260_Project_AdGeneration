from urllib import request
import simple_image_download.simple_image_download as downloader
import wikipedia
import string
import nltk
import shutil
import os
import requests
import json
import csv
import random
from nltk.corpus import wordnet as wn

NOUN_DATA = "common"

if NOUN_DATA == "general":
    with open("nouns.json", 'r') as f:
        nouns = json.load(f)

elif NOUN_DATA == "common":
    with open('nounlist.csv', 'r') as f:
        reader = csv.reader(f)
        nouns = list(reader)
        nouns = [noun[0] for noun in nouns]

with open("phrases.json", 'r') as f:
    phrases = json.load(f)

class DataCollection:
    def __init__(self, topic):
        self.topic = topic
        self.output_directory = './dataset/'
        self.limit = 5
        nltk.download('punkt')
        nltk.download('stopwords')
        self.my_downloader = downloader.Downloader()
        self.my_downloader.directory = self.output_directory
        self.my_downloader.extensions = '.jpg'

    def download_image(self):
        self.my_downloader.download(self.topic, limit=self.limit)

    def remove_existing_directory(self):
        dir_path = self.output_directory + '/' + str(self.topic)
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

    def get_phrases(self):
        return phrases

    def get_words(self, num_nouns=100, num_adj=20):
        noun_adj_dict = {}

        noun_idxs = random.sample(range(len(nouns)), num_nouns)
        for i in noun_idxs:
            adj = self.get_adjectives(nouns[i])
            if len(adj) < num_adj:
                continue
            adj_idxs = random.sample(range(len(adj)), num_adj)
            adj = [adj[j] for j in adj_idxs]
            noun_adj_dict[nouns[i]] = adj

        return noun_adj_dict
    
    def get_wikipedia_words(self):    
        try:
            text = wikipedia.summary(self.topic)
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
        

        

    def run(self):
        words_dict = self.get_words()
        if(words_dict is None):
            return None, None
        self.remove_existing_directory()
        self.download_image()
        image_paths = []
        for i in self.my_downloader.cached_urls.keys():
            image_paths.append(str(self.my_downloader.cached_urls[i][0] + '/' + i))
        return image_paths, words_dict
