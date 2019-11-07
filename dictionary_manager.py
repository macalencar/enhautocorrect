"""
Creates a dictionary for a specfic language
based on the frequency of words.
Before append a new dictionary for a new language,
make sure that you appended tha alphabeth of
this language in constants.py

--
1 - Remove item from dictionary
2 - Store pruned dictionary
3 - Thread/Multiprocessing tasks
"""

import json
import re
import os
import tarfile
from enhautocorrect.constants import word_regexes
from contextlib import closing

PATH = os.path.abspath(os.path.dirname(__file__))

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

def load_from_tar(archive_name, file_name='word_count.json'):
    """ Decompress and load the frequency dictionary """
    with tarfile.open(archive_name, 'r:gz') as tarf:
        with closing(tarf.extractfile(file_name)) as file:
            return json.load(file)

def count_words2(src_filename, lang, out_filename='word_count.json'):
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

def count_words(src_filename, lang, update=True, out_filename='word_count.json'):
    """ Analyze the input file based on the language and
        create a compressed package for further usage """
    words = get_words(src_filename, lang)
    counts = parse(words)    
    out_dict=counts
    dict_file = os.path.join(PATH, 'data/{}.tar.gz'.format(lang))        
    if update and os.path.exists(dict_file):
        old_dict = load_from_tar(dict_file)
        for k in counts.keys():
            try: old_dict[k]+=counts[k] #increment 
            except KeyError: old_dict[k]=counts[k] #append
        counts={}
        out_dict=old_dict           
    with open(out_filename, 'w') as outfile:
        json.dump(out_dict, outfile)

    with tarfile.open(dict_file, "w:gz") as compressed_file:
        compressed_file.add(out_filename)
    os.remove(out_filename)
