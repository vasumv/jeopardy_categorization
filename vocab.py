from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import numpy as np

class Vocabulary():
    def __init__(self):
        self.word_mapping = {}
        self.number_mapping = {}
        self.number = -1
        self.stemmer = SnowballStemmer("english")

    def tokenize(self, clue):
        clue = clue.lower()
        clue = word_tokenize(clue)
        stop = stopwords.words('english')
        words = [self.stemmer.stem(x) for x in clue if x.isalpha() and x not in stop and x not in {'name', 'point'}]
        return words

    def add_question(self, clue):
        words = self.tokenize(clue)
        for word in words:
            if word in self.word_mapping:
                continue
            self.number += 1
            self.word_mapping[word] = self.number
            self.number_mapping[self.number] = word

    def translate(self, clue):
        words = self.tokenize(clue)
        vector = np.zeros(self.number + 1)
        for word in words:
            if word not in self.word_mapping:
                continue
            vector[self.word_mapping[word]] += 1
        return vector






