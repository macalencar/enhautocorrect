# Python 3 Spelling Corrector
#
# Copyright 2014 Jonas McCallum.
# Updated for Python 3, based on Peter Norvig's
# 2007 version: http://norvig.com/spell-correct.html
"""
Word based methods and functions

Author: Jonas McCallum
https://github.com/foobarmus/autocorrect

Optimized by: Filip Sondej
https://github.com/fifimajster/autocorrect/

Customized by: Márcio Alencar
https://github.com/macalencar/enhautocorrect/

1 - Remove item from dictionary
2 - Store pruned dictionary
3 - Thread/Multiprocessing tasks

"""
import json
import re
import tarfile
import os
from contextlib import closing
from enhautocorrect.constants import word_regexes
from enhautocorrect.typos import Word

PATH = os.path.abspath(os.path.dirname(__file__))

def load_from_tar(archive_name, file_name='word_count.json'):
    """ Decompress and load the frequency dictionary """
    with tarfile.open(archive_name, 'r:gz') as tarf:
        with closing(tarf.extractfile(file_name)) as file:
            return json.load(file)

def get_words(filename, lang):
    """ Gets the words from input file  based on word_regexes
        associated to the language """
    word_regex = word_regexes[lang]
    #alphabeth_regex = r'(\.|^|<|"|\'|\(|\[|\{\s*)' + word_regexes[lang] # '(\.|^|<|"|\'|\(|\[|\{\s*)'
    count_words=0
    with open(filename) as file:
        for line in file:
            #line = re.sub(alphabeth_regex, '', line.lower())
            for word in re.findall(word_regex, line):
                if word.strip():
                    yield word

def parse(words):
    """ Stores the words frequency """
    counts = dict()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def save_dictionary(freq_dict, dict_file, out_filename='word_count.json'):
    with open(out_filename, 'w') as outfile:
        json.dump(freq_dict, outfile)
    with tarfile.open(dict_file, "w:gz") as compressed_file:
        compressed_file.add(out_filename)
    os.remove(out_filename)        

def count_words(src_filename, lang, update=True):
    """ Analyze the input file based on the language and
        create a compressed package for further usage """
    words = get_words(src_filename, lang)
    counts = parse(words)    
    freq_dict=counts
    dict_file = os.path.join(PATH, 'data/{}.tar.gz'.format(lang))        
    if update and os.path.exists(dict_file):
        old_dict = load_from_tar(dict_file)
        for k in counts.keys():
            try: old_dict[k]+=counts[k] #increment 
            except KeyError: old_dict[k]=counts[k] #append
        counts={}
        freq_dict=old_dict          
    save_dictionary(freq_dict, dict_file)

class Speller:
    """ Main class that loads the dicitonary based on the language.
        It is possible to reduce the dictionary size by eliminating
        the words with frequency value lower than threshold value """

    def __init__(self, lang='en', threshold=0):
        self.threshold = threshold
        self.dict_file = os.path.join(PATH, 'data/{}.tar.gz'.format(lang))
        self.nlp_data = load_from_tar(self.dict_file)
        self.lang = lang
        if threshold > 0:
            self.prune_dictionary(threshold)

    def prune_dictionary(self, threshold):
        if threshold > 0:
            print('Original number of words: {}'.format(len(self.nlp_data)))
            self.nlp_data = {k: v for k, v in self.nlp_data.items() if v > threshold}
            print('After applying threshold: {}'.format(len(self.nlp_data)))

    def existing(self, words):
        """{'the', 'teh'} => {'the'}"""
        return set(word for word in words
                   if word in self.nlp_data)

    def get_frequency(self, word):
        """{word, frequecy}"""
        if word in self.nlp_data:
            return self.nlp_data[word]
        return 0

    def remove_words(self, words_list, permanent=False):
        for word in words_list:
            try:
                del self.nlp_data[word]                
            except KeyError:
                print("Word",word,"not found")
        if permanent:    
            save_dictionary(self.nlp_data, self.dict_file)
    
    def candidates(self, word, max_suggestions=3, labels=False):
        """
        >>> Speller.candidates("gxt")
        [('get', 0.40018832391713743), ('got', 0.2532956685499058), ('gut', 0.01224105461393597)]
        >>>
        """
        word_obj = Word(word, self.lang)
        words_lst = (self.existing([word]) or
                     self.existing(word_obj.typos()) or
                     self.existing(word_obj.double_typos()) or
                     [word])

        words_lst=sorted(words_lst, key=self.nlp_data.get, reverse=True)
        if word in words_lst:
            return None

        if not labels:
            return words_lst[:max_suggestions]

        words_prob = list()
        wp_total = sum (self.get_frequency(w) for w in words_lst) + 1 #, key=self.nlp_data.get))
        for candidate in words_lst:
            words_prob.append({"term":candidate, "probability":self.get_frequency(candidate)/wp_total})
        return words_prob[:max_suggestions]

    def analyze_sentence(self, sentence, max_suggestions=3, labels=False):
        """ gives a suggestion for each wrong word in sentence """
        report={}
        if labels:
            report={"sentence":sentence,"issues":list()}

        #for word in re.findall(word_regexes[self.lang], sentence):
        for word in re.findall(r'\w+', sentence.lower()):
            candidates_list = self.candidates(word, max_suggestions, labels)
            if candidates_list:
                if labels:
                    report["issues"].append({"wrongTerm":word, "suggestions":candidates_list})
                else:
                    report[word]=candidates_list
        if labels:
            if len(report["issues"]) > 0:
                return report
            return None
        else: 
            return report or None


    def autocorrect_word(self, word):
        """most likely correction for everything up to a double typo"""
        word_obj = Word(word, self.lang)
        candidates = (self.existing([word]) or
                      self.existing(word_obj.typos()) or
                      self.existing(word_obj.double_typos()) or
                      [word])
        return max(candidates, key=self.nlp_data.get)

    def autocorrect_sentence(self, sentence):
        """return the correct sentence after each word pass throught autocorrect_word"""
        return re.sub(word_regexes[self.lang],
                      lambda match: self.autocorrect_word(match.group(0)),
                      sentence.lower())

    __call__ = autocorrect_sentence
