import nltk
from nltk import word_tokenize
import sys
import os
import string


def main():
    
    str = "Roy, is a boy"
    stop_words = nltk.corpus.stopwords.words("english")

    words = []
    for word in word_tokenize(str):
        if word not in string.punctuation and word not in stop_words:
           words.append(word.lower()) 
    print(words)


main()