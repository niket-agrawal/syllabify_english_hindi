# Python benchmarks for English/Hindi syllable counters and syllabification methods

## 1. English syllabification methods

**1.1 There exists mainly 4 categories of methods:**
- Dictionary searches, e.g. CMU dict
- Hyphenation methods, e.g. PyHyphen - https://www.tug.org/docs/liang/liang-thesis.pdf
- ML based approaches, non explanability
- Rule based approaches, fast and might be inaccurate, e.g. Sonority Sequencing by nltk

**1.2 We have tested the following packages and libraries for English:**
- `nltk` **sonority** based and **cmu** dict
- `indic` lib
- hyphenation libraries, `pyphen` and `hyphenate`
- `spacy` machine learning models, **spacy_syllable** and **nlp pipeline**
- machine learning models, `meow25` and `bigphoney`
- user contributions over internet, `basirico`, `anonuser1`, `abigailb`, `hauntninja` and `tarun`
- misc libs, `syllapy` and `syllables`

**1.3 Some packages syllabify and count, others just count syllables:**
| **Method Type**             | **Implementation Type** | **Implementation Name**       | **References** |
|-----------------------------|-------------------------|-------------------------------|----------------|
| **Syllabification + Count** | Library                 | nltk (sonority-based)         | [nltk sonority](https://www.nltk.org/api/nltk.tokenize.sonority_sequencing.html) |
|                             |                         | indic lib                     | [libindic](https://github.com/libindic/libindic-utils) |
|                             | Hyphenation Library     | pyphen                        | [pyphen.org](https://pyphen.org/) · [baeldung](https://www.baeldung.com/cs/syllabification-nltk-pyphen) |
|                             |                         | hyphenate                     | [StackOverflow](https://stackoverflow.com/a/61469194) · [nedbatchelder](https://nedbatchelder.com/code/modules/hyphenate.html) |
|                             | Machine Learning Model  | spaCy syllable                | [StackOverflow](https://stackoverflow.com/a/67861539) |
|                             |                         | spaCy nlp (same little faster)| [spaCy syllables project](https://spacy.io/universe/project/spacy_syllables) |
| **Count Only**              | User Contributed        | basirico                      | [StackOverflow](https://stackoverflow.com/a/5615724) |
|                             |                         | anonuser1                     | [StackOverflow](https://stackoverflow.com/a/52466549) |
|                             |                         | abigailb                      | [StackOverflow](https://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word) |
|                             |                         | hauntninja                    | [DataScience SE](https://datascience.stackexchange.com/a/89312) |
|                             |                         | tarun – sylco                 | [StackOverflow](https://stackoverflow.com/a/50851189) |
|                             | Library                 | nltk (cmudict)                | [StackOverflow](https://stackoverflow.com/a/5876365) · [Google Groups](https://groups.google.com/g/nltk-users/c/mCOh_u7V8_I) |
|                             |                         | syllapy                       | [PyPI](https://pypi.org/project/syllapy/) |
|                             |                         | syllables                     | [PyPI](https://pypi.org/project/syllables/) |
|                             | Machine Learning Model  | meow25                        | [GitHub](https://github.com/meooow25/syllable) · [Notebook](https://github.com/meooow25/syllable/blob/master/prepare.ipynb) |
|                             |                         | bigphoney                     | [StackOverflow](https://stackoverflow.com/a/51142947) · [Kaggle](https://www.kaggle.com/code/reppic/predicting-english-pronunciations) · [GitHub](https://github.com/repp/big-phoney) |


**1.4 Results**
**Benchmarking result**:

<table>
<tr>
<td> 

Dataset 1 - CMU dict

| function                  | accuracy | time_seconds |
| ------------------------- | -------: | -----------: |
| n_syllable_MLbigphone     | 0.994192 |   381.262619 |
| n_syllable_MLmeow25       | 0.956357 |   861.477137 |
| n_syllable_hauntninja     | 0.899235 |     6.629049 |
| n_syllable_tarunsylco     | 0.858078 |     7.050942 |
| n_syllable_syllapy        | 0.835673 |     6.528642 |
| n_syllable_abigailb       | 0.827986 |     6.025062 |
| n_syllable_basirico       | 0.815658 |     5.872316 |
| n_syllable_syllables      | 0.787761 |    10.954960 |
| n_syllable_anonuser1      | 0.783379 |     6.384894 |
| syllable_sonority         | 0.751788 |     9.441220 |
| syllable_indic            | 0.751432 |    10.782334 |
| syllable_MLspacynlp       | 0.609356 |   598.432799 |
| syllable_hyphen_hyphenate | 0.599976 |     7.833818 |
| syllable_hyphen_pyphen    | 0.530039 |    10.408393 |

</td>
<td>

Dataset 2 - Random from Github

| function                  | accuracy | time_seconds |
| ------------------------- | -------: | -----------: |
| n_syllable_MLbigphone     | 0.981080 |   256.622477 |
| n_syllable_MLmeow25       | 0.975795 |    52.691667 |
| n_syllable_hauntninja     | 0.944615 |     0.443599 |
| n_syllable_tarunsylco     | 0.901173 |     0.444649 |
| n_syllable_syllapy        | 0.895466 |     0.404628 |
| n_syllable_abigailb       | 0.854138 |     0.388002 |
| syllable_MLspacynlp       | 0.851707 |    38.976495 |
| syllable_hyphen_hyphenate | 0.841560 |     0.510535 |
| n_syllable_anonuser1      | 0.836909 |     0.423057 |
| n_syllable_basirico       | 0.827291 |     0.378642 |
| syllable_indic            | 0.785329 |     0.676891 |
| n_syllable_syllables      | 0.763450 |     0.726379 |
| syllable_sonority         | 0.742416 |     0.642038 |
| syllable_hyphen_pyphen    | 0.730155 |     0.457547 |

</td>
</tr>
</table>


### To be implemented:
- Gold standard is dictionary (human intervention)
- Web based approach, apis etc. (https://stackoverflow.com/questions/10414957/using-python-to-find-syllables/10416028#10416028)
     - https://www.howmanysyllables.com/syllables/table
     - https://www.wordcalc.com/index.php
