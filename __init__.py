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
from difflib import SequenceMatcher
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
        the words smaller then threshold value """

    def __init__(self, threshold=0, lang='en'):
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

    def candidates(self, word, max_suggestions=3):
        """
        >>> Speller.candidates("gxt")
        [('get', 0.40018832391713743), ('got', 0.2532956685499058), ('gut', 0.01224105461393597)]
        >>>
        """
        word_obj = Word(word, self.lang)
        words_lst = list()
        words_lst += self.existing([word])
        words_lst += self.existing(word_obj.typos())
        words_lst += self.existing(word_obj.double_typos())
        words_lst += [word.lower()]

        if word not in words_lst:
            words_prob = dict()
            for candidate in words_lst:
                words_prob[candidate] = self.get_frequency(candidate)
            wp_total = 1 + sum(words_prob.values())
            for candidate in words_lst:
                similarity = SequenceMatcher(None, candidate.lower(), word.lower()).ratio()
                words_prob[candidate] = (words_prob[candidate]/wp_total) * similarity

            words_prob = sorted(words_prob.items(), key=lambda x: x[1], reverse=True)
            return words_prob[:max_suggestions]
        return None

    def analyze_sentence(self, sentence, max_suggestions=3):
        """ gives a suggestion for each wrong word in sentence """
        ocurrences = {}
        for word in re.findall(word_regexes[self.lang], sentence):
            candidates_list = self.candidates(word, max_suggestions)
            if candidates_list:
                ocurrences[word] = candidates_list
        return ocurrences

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
                      sentence)

    __call__ = autocorrect_sentence
