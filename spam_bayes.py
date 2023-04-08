import pandas as pd
import numpy as np
from nltk import word_tokenize
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from itertools import chain

class NaiveBayesSpamFilter:
    def __init__(self):
        pass
    
    def text_transform(self, text):
        stemmer = PorterStemmer()
        eng_stop_words = stopwords.words("english")
        punct = string.punctuation
        text = text.lower()
        text = word_tokenize(text)
        y = []      
        for i in text:
            if i.isalnum():
                y.append(i)
        text = y[:]
        y.clear()   
        for i in text:
            if i not in eng_stop_words and i not in punct:
                y.append(i)            
        text = y[:]
        y.clear()  
        for i in text:
            y.append(stemmer.stem(i))
    
        return " ".join(y)
    
    def split_tranfsormed_text(self, data):
        splited = list(map(self.text_transform, data.astype(str)))
        splited = [email.split() for email in splited]
        return splited
    
    def preprocess_data(self, data):
        splited = self.split_tranfsormed_text(data)
        prep_data = list(set(chain(*splited)))
        return prep_data
    
    def compute_spamicity(self):
        dict_spamicity = {}
        splited = self.split_tranfsormed_text(self.train_spam)
        prep_data = self.preprocess_data(self.train_spam)
        for word in prep_data:
            emails_with_word = 0
            for message in splited:
                if word in message:
                    emails_with_word += 1
            total_spam = len(self.train_spam)
            spamicity = (emails_with_word + 1) / (total_spam + 2)
            dict_spamicity[word] = spamicity
            
        return dict_spamicity
    
    def compute_hamicity(self):
        dict_hamicity = {}
        splited = self.split_tranfsormed_text(self.train_ham)
        pred_data = self.preprocess_data(self.train_ham)
        for word in pred_data:
            emails_with_word = 0
            for message in splited:
                if word in message:
                    emails_with_word += 1
            total_ham = len(self.train_ham)
            hamicity = (emails_with_word + 1) / (total_ham + 2)
            dict_hamicity[word] = hamicity
        
        return dict_hamicity  
    
    
    def compute_probas(self, reduced_sentences):
        pr_sw = []
        dict_spamicity = self.compute_spamicity()
        dict_hamicity = self.compute_hamicity()
        prob_spam = 0.5
        prob_ham = 0.5
        for message in reduced_sentences:
            pr_sw.append([])
        
        counter = 0
        for message in reduced_sentences:
            for word in message:
                if word in list(dict_spamicity.keys()) and word in list(dict_hamicity.keys()):
                    pr_sw[counter].append(dict_spamicity[word] * prob_spam / (dict_spamicity[word] * prob_spam + dict_hamicity[word] * prob_ham))
            counter += 1
        return pr_sw
    
    def mult_list(self, lst):
        res = 1
        for item in lst:
            res *= item
            
        return res
    
    def fit(self, train_spam, train_ham):
        self.train_spam = train_spam
        self.train_ham = train_ham
    
    def predict(self, test_contents):
        reduced_sentences = []
        prep_spam = self.preprocess_data(self.train_spam)
        prep_ham = self.preprocess_data(self.train_ham)
        test = self.split_tranfsormed_text(test_contents)
        for sentence in test:
            words = []
            for word in sentence:
                if word in prep_spam:
                    words.append(word)
                elif word in prep_ham:
                    words.append(word)
            reduced_sentences.append(words)
        
        pr_sw = self.compute_probas(reduced_sentences)
        pred = [1 if self.mult_list(lst) >= 0.5 else 0 for lst in pr_sw]
        
        return pred