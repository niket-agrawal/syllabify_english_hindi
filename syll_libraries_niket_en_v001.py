# Script to quickly benchmark syllabification libraries and codes on
# Version 0.0.1 fixed on 22 Aug 2025

import spacy
import pyphen
import hyphenate
import syllapy
import syllables
import re, sys
from nltk.corpus import cmudict
from nltk.tokenize import SyllableTokenizer
from libindic.syllabifier import Syllabifier
from spacy_syllables import SpacySyllables
sys.path.append("syllable-master")
from syllable import CmudictSyllableCounter, ModelSyllableCounter

# ######## Hack JUGAD for importing Tensorflow ##################################
# import os
# import ctypes

# # Force Windows to include System32 in DLL search path
# os.add_dll_directory(r"C:\Windows\System32")

# # Optionally also add TensorFlow's bin path
# tf_bin = r"C:\programs_pkgs\pyth\env1_iitkcgs\Lib\site-packages\tensorflow"
# if os.path.exists(tf_bin):
#     os.add_dll_directory(tf_bin)

# # Force reloading kernel DLL search path logic
# ctypes.windll.kernel32.SetDllDirectoryW(None)

# import tensorflow as tf
# # print(tf.__version__)
from big_phoney import BigPhoney
# ###############################################################################


# https://www.nltk.org/api/nltk.tokenize.sonority_sequencing.html
SSP = SyllableTokenizer()
def syllable_sonority(word):
    syll = SSP.tokenize(word)
    return {"word":word, "sylls":syll, "nsyll":len(syll)}

# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
# SpacySyllables is pretty decent, just be aware that it's unfortunately not perfect. 
# "eighty" returns ['eighty'] and "universal" returns ['uni', 'ver', 'sal']. 
# This is due to the underlying library (Pyphen) having a default of 2 characters for the first and last syllables.
# Load the NLP model once
nlp1 = spacy.load('en_core_web_md')
syllables1 = SpacySyllables(nlp1)
nlp1.add_pipe('syllables', after='tagger')
def syllable_MLspacysyll(word):
    token = nlp1(word)[0]
    syll = token._.syllables
    nsyll = 0 if syll is None else len(syll)
    return {"word":word, "sylls":syll, "nsyll":nsyll}


# Spacy web
# https://spacy.io/universe/project/spacy_syllables
# Load the NLP model once
nlp2 = spacy.load("en_core_web_md")
nlp2.add_pipe("syllables", after="tagger")
assert nlp2.pipe_names == ["tok2vec", "tagger", "syllables", "parser",  "attribute_ruler", "lemmatizer", "ner"]
def syllable_MLspacynlp(word):    
    doc = nlp2(word)
    data = [(token.text, token._.syllables, token._.syllables_count) for token in doc]
    data = data[0]
    syll = data[1]
    nsyll = len(syll) if syll is not None else 0 
    return {"word":word, "sylls":syll, "nsyll":nsyll}

# https://github.com/libindic/libindic-utils
instance = Syllabifier()
def syllable_indic(word):
    syll = instance.syllabify(word)
    syll = syll.strip()
    syll = syll.replace('/','_').replace('-','_')
    syll = syll.split('_')
    return {"word":word, "sylls":syll, "nsyll":len(syll)}

# https://pyphen.org/ # Insert hyphens into the word to indicate syllable breaks
# https://www.baeldung.com/cs/syllabification-nltk-pyphen
dic = pyphen.Pyphen(lang='en')
def syllable_hyphen_pyphen(word):
    syll = dic.inserted(word).replace('-', '-')
    syll = syll.split('-')
    return {"word":word, "sylls":syll, "nsyll":len(syll)}

# https://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
# Based on  Francis Mark Liang's hyphenation algorithm: https://nedbatchelder.com/code/modules/hyphenate.py
# Also used in Tex, fast but error prone (quick and dirty)
def syllable_hyphen_hyphenate(word):
    syll = hyphenate.hyphenate_word(word)
    return {"word":word, "sylls":syll, "nsyll":len(syll)}


# https://stackoverflow.com/questions/5876040/number-of-syllables-for-words-in-a-text
# https://groups.google.com/g/nltk-users/c/mCOh_u7V8_I
d_cmu = cmudict.dict()
def n_syllable_cmudict(word):
    if word.lower() not in d_cmu:
        return {"word":word, "nsyll":None}    
    else:
        # return d_cmu[word.lower()]
        # return [len(list(y for y in x if y[-1].isdigit())) for x in d_cmu[word.lower()]]
        nsyll = max([len([y for y in x if y[-1].isdigit()]) for x in d_cmu[word.lower()]])
        return {"word":word, "nsyll":nsyll}


# https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word/4103234#4103234
# Joe Basirico, converted to python using Duck.ai
def n_syllable_basirico(word):
    vowels = "aeiouy"
    numVowels = 0
    lastWasVowel = False
    for wc in word:
        foundVowel = False
        for v in vowels:
            if v == wc:
                if not lastWasVowel:
                    numVowels += 1  # don't count diphthongs
                foundVowel = lastWasVowel = True
                break
        
        if not foundVowel:  # If full cycle and no vowel found, set lastWasVowel to false
            lastWasVowel = False
            
    if len(word) > 2 and word[-2:] == "es":  # Remove es - it's "usually" silent (?)
        numVowels -= 1
    elif len(word) > 1 and word[-1:] == "e":  # remove silent e
        numVowels -= 1
        
    return {"word":word, "nsyll":numVowels}
    # Another implementation of same algo; ideally should return same result
    # def count_syllables(word):
    #     vowels = 'aeiouy'
    #     num_vowels = 0
    #     last_was_vowel = False
    #     for char in word:
    #         found_vowel = False
    #         if char in vowels:
    #             if not last_was_vowel:
    #                 num_vowels += 1
    #                 last_was_vowel = True
    #                 found_vowel = True
    #             else:
    #                 found_vowel = True
    #         if not found_vowel:
    #             last_was_vowel = False
    #     # Remove 'es' if it's usually silent
    #     if len(word) > 2 and word.endswith('es'):
    #         num_vowels -= 1
    #     # Remove silent 'e'
    #     elif len(word) > 1 and word.endswith('e'):
    #         num_vowels -= 1
    #     return num_vowels

# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word/4103234#4103234
# user5825851
def n_syllable_anonuser1(word):
    cleanText = ""
    for ch in word:
        if ch in "abcdefghijklmnopqrstuvwxyz'’":
            cleanText += ch
        else:
            cleanText += " "

    asVow    = "aeiouy'’"
    dExep    = ("ei","ie","ua","ia","eo")
    theWords = cleanText.lower().split()
    allSylls = 0
    for inWord in theWords:
        nChar  = len(inWord)
        nSyll  = 0
        wasVow = False
        wasY   = False
        if nChar == 0:
            continue
        if inWord[0] in asVow:
            nSyll += 1
            wasVow = True
            wasY   = inWord[0] == "y"
        for c in range(1,nChar):
            isVow  = False
            if inWord[c] in asVow:
                nSyll += 1
                isVow = True
            if isVow and wasVow:
                nSyll -= 1
            if isVow and wasY:
                nSyll -= 1
            if inWord[c:c+2] in dExep:
                nSyll += 1
            wasVow = isVow
            wasY   = inWord[c] == "y"
        if inWord.endswith(("e")):
            nSyll -= 1
        if inWord.endswith(("le","ea","io")):
            nSyll += 1
        if nSyll < 1:
            nSyll = 1
        # print("%-15s: %d" % (inWord,nSyll))
        allSylls += nSyll
    syll_count = allSylls/len(theWords)
    return {"word":word, "nsyll":syll_count}

# https://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
# AbigailB
def n_syllable_abigailb(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return {"word":word, "nsyll":count}

# https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
# hauntsaninja
def n_syllable_hauntninja(word):
    VOWEL_RUNS = re.compile("[aeiouy]+", flags=re.I)
    EXCEPTIONS = re.compile(
        # fixes trailing e issues:
        # smite, scared
        "[^aeiou]e[sd]?$|"
        # fixes adverbs:
        # nicely
        + "[^e]ely$",
        flags=re.I
    )
    ADDITIONAL = re.compile(
        # fixes incorrect subtractions from exceptions:
        # smile, scarred, raises, fated
        "[^aeioulr][lr]e[sd]?$|[csgz]es$|[td]ed$|"
        # fixes miscellaneous issues:
        # flying, piano, video, prism, fire, evaluate
        + ".y[aeiou]|ia(?!n$)|eo|ism$|[^aeiou]ire$|[^gq]ua",
        flags=re.I
    )

    vowel_runs = len(VOWEL_RUNS.findall(word))
    exceptions = len(EXCEPTIONS.findall(word))
    additional = len(ADDITIONAL.findall(word))
    nsyll = max(1, vowel_runs - exceptions + additional)

    return {"word":word, "nsyll":nsyll}

# https://stackoverflow.com/questions/46759492/syllable-count-in-python
# Tarun
def n_syllable_tarunsylco(word) :
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious','crucial']
    exception_del = ['fortunately','unfortunately']

    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']

    pre_one = ['preach']

    syls = 0 #added syllable number
    disc = 0 #discarded syllable number

    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        syls = 1
        # return syls
        return {"word":word, "nsyll":syls}

    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed" :
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                pass
            else :
                disc+=1

    #3) discard trailing "e", except where ending is "le"  

    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']

    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in le_except :
            pass

        else :
            disc+=1

    #4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
    disc+=doubleAndtripple + tripple

    #5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        syls+=1

    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        syls +=1

    #8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    syls+=1

    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui" :
        syls+=1

    if word[:2] == "bi" and word[2] in "aeoui" :
        syls+=1

    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian" : 
    #and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian" :
            pass
        else :
            syls+=1

    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui' :

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
            syls+=1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
            pass
        else :
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in pre_one :
            pass
        else :
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]

    if word[-3:] == "n't" :
        if word in negative :
            syls+=1
        else :
            pass   

    #14) Handling the exceptional words.

    if word in exception_del :
        disc+=1

    if word in exception_add :
        syls+=1     

    # calculate the output
    nsyll = numVowels - disc + syls
    return {"word":word, "nsyll":nsyll}


# https://pypi.org/project/syllapy/
# Seems like direct lookup from an unknown dict, and if not found, using a custom code
def n_syllable_syllapy(word):
    nsyll = syllapy.count(word)
    return {"word":word, "nsyll":nsyll}

# https://pypi.org/project/syllables/
# Syllables is a fast, simple syllable estimator for Python. 
# It's intended for use in places where speed matters. For situations where accuracy matters, please consider the cmudict Python library instead.
def n_syllable_syllables(word):
    nsyll = syllables.estimate(word)
    return {"word":word, "nsyll":nsyll}

# ML Based appraoch
# https://github.com/meooow25/syllable/blob/master/prepare.ipynb
# https://github.com/meooow25/syllable
# Load the NLP model once
msc = ModelSyllableCounter()
def n_syllable_MLmeow25(word):
    # csc = CmudictSyllableCounter()
    # csc.count_syllables('family')
    nsyll = msc.count_syllables(word)
    nsyll = nsyll[0] if nsyll != () else 0
    return {"word":word, "nsyll":nsyll}


# ML based approach
# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word/4103234#4103234
# https://www.kaggle.com/code/reppic/predicting-english-pronunciations
# https://github.com/repp/big-phoney
phoney = BigPhoney()
def n_syllable_MLbigphone(word):
    nsyll = phoney.count_syllables(word)
    return {"word":word, "nsyll":nsyll}


# https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
# Best approach - Catch the key error you get when the word is not found in cmu's dictionary as below:
# shantanuSpark
# d_cmu = cmudict.dict()
    
# def nsyl_shan(word):
#     try:
#         return [len(list(y for y in x if y[-1].isdigit())) for x in d_cmu[word.lower()]]
#     except KeyError:
#         #if word not found in cmudict
#         return syllables(word) # AbigailB

# for word in word_list:
#     syll = nsyl_shan(word)
#     print(word, syll)



# https://github.com/textstat/textstat/blob/main/textstat/backend/counts/_count_syllables.py
# import textstat
# In summary, this code attempts to count the syllables of a word using the CMU Pronouncing Dictionary. 
# If it fails to retrieve the phonetic representation (due to various potential errors), it falls back on using the pyphen library to estimate the syllable count based on hyphenation positions. 
# The final result is stored in the variable count.
# text = "amsterdam"
# textstat.syllable_count(text)