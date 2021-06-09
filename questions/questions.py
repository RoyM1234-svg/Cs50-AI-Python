from re import X
import nltk
from nltk import word_tokenize
import sys
import os
import string
import math

from nltk.sem.relextract import roles_demo


FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dir_dict = dict()
    for f in os.listdir(directory):
        temp_file = open(os.path.join(directory,f),'r',encoding="utf8")
        dir_dict[f] = temp_file.read()
        temp_file.close()
    return dir_dict
            
   
            
     

    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # nltk.download('stopwords')
    # nltk.download('punkt')
    stop_words = nltk.corpus.stopwords.words("english")
    words = []
    for word in  word_tokenize(document):
        if word not in string.punctuation and word.lower() not in stop_words:
            words.append(word)

    
    return words
    # raise NotImplementedError

def is_appeared(word, document):
    if word in document:
        return True
    return False
def get_log_value(num_of_documents,num_of_appearence):
    return math.log(num_of_documents / num_of_appearence)

def get_num_appearence(word,documents):
    num_of_appearence = 0
    for document in documents:
        if word in document:
            num_of_appearence += 1
    return num_of_appearence 

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    Idfs_dict = dict()
    for words_bag in documents.values():
        for word in words_bag:
            if word in Idfs_dict.keys():
                continue
            else:
                Idfs_dict[word] = get_log_value(len(documents),get_num_appearence(word,documents.values()))
    return Idfs_dict

    # raise NotImplementedError

def count_appearence(word,document):
    x = 0
    for w in document:
        if w == word:
            x += 1
    return x
    

def get_n_top(files,n):
    files_list = []
    temp = sorted(files.items(), key = lambda item : item[1], reverse = True)
    for element in temp:
        files_list.append(element[0])
    return files_list[:n]


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {file : 0 for file in files.keys()}
    for word in query:
        for file, content in files.items():
            tf_idfs[file] += count_appearence(word,content) * idfs[word]
    
    files_list = get_n_top(tf_idfs, n)
    return files_list
    

    # raise NotImplementedError


def get_query_term_density(query, sentence):
    density = 0
    for word in query:
        if word in sentence:
            density += 1 / len(sentence)
    return density


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_idfs = {sentence : 0 for sentence in sentences.keys()}
    for word in query:
        for sentence, content in sentences.items():
            if word in content:
                sentences_idfs[sentence] += idfs[word]
    sentences_list = get_n_top(sentences_idfs, n)
    return sentences_list



if __name__ == "__main__":
    main()
