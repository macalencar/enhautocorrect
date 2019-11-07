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


class Speller:
    """ Main class that loads the dicitonary based on the language.
        It is possible to reduce the dictionary size by eliminating
        the words with frequency value lower than threshold value """

    def __init__(self, lang='en', threshold=0):
        self.threshold = threshold
        dic_file = os.path.join(PATH, 'data/{}.tar.gz'.format(lang))
        self.nlp_data = load_from_tar(dic_file)
        self.lang = lang

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
