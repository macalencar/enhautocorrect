"""
Creates a dictionary for a specfic language
based on the frequency of words.
Before append a new dictionary for a new language,
make sure that you appended tha alphabeth of
this language in constants.py
"""
import json
import re
import os
import tarfile
from enhautocorrect.constants import word_regexes

PATH = os.path.abspath(os.path.dirname(__file__))

def get_words(filename, lang):
    """ Gets the words from input file  based on word_regexes
        associated to the language """
    word_regex = word_regexes[lang]
    capitalized_regex = r'(\.|^|<|"|\'|\(|\[|\{)\s*' + word_regexes[lang]
    with open(filename) as file:
        for line in file:
            line = re.sub(capitalized_regex, '', line)
            for word in re.findall(word_regex, line):
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

def count_words(src_filename, lang, out_filename='word_count.json'):
    """ Analyze the input file based on the language and
        create a compressed package for further usage """
    words = get_words(src_filename, lang)
    counts = parse(words)
    with open(out_filename, 'w') as outfile:
        json.dump(counts, outfile)
    dict_file = os.path.join(PATH, 'data/{}.tar.gz'.format(lang))
    with tarfile.open(dict_file, "w:gz") as compressed_file:
        compressed_file.add(out_filename)
    os.remove(out_filename)
