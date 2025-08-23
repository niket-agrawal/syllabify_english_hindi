# Script to quickly benchmark syllabification libraries and codes on
# Version 0.0.1 fixed on 23 Aug 2025

import time, os, sys
import pandas as pd

from libindic.syllabifier import Syllabifier

sys.path.append("../")
import HindiWordFeatures as hi_feature #add word length for Hindi

# https://github.com/libindic/libindic-utils
instance = Syllabifier()
def syllable_indic_hi(word):
    syll = instance.syllabify(word)
    return {"word":word, "sylls":syll, "nsyll":len(syll)}

def syllable_anurag_sascha(word):
    syll = hi_feature.word_segment_anurag_sascha(word)
    return {"word":word, "sylls":syll[0], "nsyll":syll[1]}

def syllable_niket_wuggy(word):
    syll = hi_feature.word_segment_niket(word)
    return {"word":word, "sylls":syll, "nsyll":len(syll)}

# https://stackoverflow.com/a/47123580
def syllable_shantanoo(word):
    syll = hi_feature.word_segment_shantanoo(word)
    syll = list(syll)
    return {"word":word, "sylls":syll, "nsyll":len(syll)}