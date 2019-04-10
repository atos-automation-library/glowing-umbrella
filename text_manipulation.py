# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import nltk
from nltk.corpus import gutenberg
from pprint import pprint

alice = gutenberg.raw(fileids='carroll-alice.txt')
sample_text = 'we will discuss briefly about the basic syntax, structure and design philosophies. There is a defined hierarchical syntax for Python code which you should remember when writing code! Python is a really powerful programming language!'

# print(len(alice))
# print(alice[0:100])

default_st = nltk.sent_tokenize

alice_sentences = default_st(alice)
sample_sentences = default_st(text=sample_text)

# print("total sentences in sample_text: ", len(sample_sentences))

from nltk.corpus import europarl_raw

german_text = europarl_raw.german.raw(fileids='ep-00-01-17.de')

# Total characters in the corpus
# print(len(german_text))

# First 100 characters in the corpus
# print(german_text[0:100])

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits0(word):
    "Return all strings that are zero edits away"
    return {word}

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # print(splits)
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # print(inserts)
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return set((e2 for e1 in edits1(word) for e2 in edits1(e1)))

def correct(word):
    """ 
    Get the best correct spelling for the input word
    """
    # Priority is for edit distance 1, then 2, then 3
    candidates = (known(edits0(word)) or known(edits1(word)) or known(edits2(word)) or [word])
    return max(candidates, key=WORDS.get)

def correct_match(match):
    """ 
    spell correct word in match, 
    and preserver proper uppre/lower/title case
    """
    word = match.group()
    def case_of(text):
        """
        Return the case function appropriate
        for text: upper / lower / title or just str
        """
        return (str.upper if text.isupper() else str.lower if text.islower() else str.title if text.istitle() else str)
    
    return case_of(word)(correct(word.lower()))

def correct_text_generic(text):
    """
    Correct all the words within a text, 
    returning the corrected text
    """
    return re.sub('[a-zA-Z]+', correct_match, text)

print(correct_text_generic("FIANLLYY the Stllye is fatnastci"))

from hunspell import Hunspell
h = Hunspell()

print(h.suggest("margarita"))

