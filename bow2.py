import json
import sqlite3

positive = []
negative = []


class Sentence:
    '''object representing a sentence'''
    def __init__(self, text):
        '''format the passed in text'''
        self.text = text.lower()
        self.__dict_repr = {}
        self.words = self.text.split(" ") #can be adjusted for N-gram models
        #TODO: regex expression to remove punctuation and numbers

    def tokenize(self):
        '''take a string and turn it into a dictionary with the word as the key, and the frequency as the value'''

        for word in self.words:
            try:
                self.__dict_repr[word] += 1
            except KeyError:
                self.__dict_repr.update({word: 1})

        return self.__dict_repr

    def length(self):
        return len(self.words)

    def weight(self):
        '''assigns a weight to each word based on its frequency'''
        total_length = len(self.words) #total number of words in the sentence
        for key,value in self.__dict_repr.items():
            self.__dict_repr[key] = value / total_length

    @property
    def dict_repr(self):
        self.tokenize()

        #self.weight()
        return self.__dict_repr



class Sentiment:
    '''uses Sentence objects to train a model and understand the sentiment of a given Sentence'''


    def __init__(self):
        conn = sqlite3.connect('training.db')
        self.c = conn.cursor()

        self.positive = {}
        self.negative = {}
        db_query = self.c.execute("SELECT * FROM training_data")
        self.training_data = db_query.fetchall()

        #print(self.training_data)



    def train(self):
        '''uses a list of Sentence objects to build the model'''

        for obj in self.training_data:
            if obj[1] == True:
                sen = Sentence(obj[0])

                for word,freq in sen.dict_repr.items():
                    try:
                        self.positive[word] += freq
                    except KeyError:
                        self.positive.update({word:freq})

            else:
                sen = Sentence(obj[0])
                for word,freq in sen.dict_repr.items():
                    try:
                        self.negative[word] += freq
                    except KeyError:
                        self.negative.update({word:freq})

        positive_keys = list(self.positive.keys())
        negative_keys = list(self.negative.keys())
        duplicate_keys = []
        for positive_key in positive_keys:
            for negative_key in negative_keys:
                if positive_key == negative_key:
                    duplicate_keys.append(positive_key)

        for dupe in duplicate_keys:
            del self.positive[dupe]
            del self.negative[dupe]

        print(self.positive)



    def analyze(self):
        text = input("Sentence to analyze: ")
        total_count = len(self.positive.keys()) + len(self.negative.keys())
        score = 0.00
        sen = Sentence(text)
        for word in sen.words:
            if word in self.positive.keys():
                score += self.positive[word] / total_count
            elif word in self.negative.keys():
                score -= self.negative[word] / total_count
        if score > 0:
            return "Positive"
        elif score < 0:
            return "Negative"
        else:
            return "Inconclusive"

s = Sentiment()
s.train()
while True:
    print(s.analyze())
