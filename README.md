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
| **Method Type**             | **Implementation Type** | **Implementation Name**       |
|-----------------------------|-------------------------|-------------------------------|
| **Syllabification + Count** | Library                 | nltk (sonority-based)         |
|                             |                         | indic lib                     |
|                             | Hyphenation Library     | pyphen                        |
|                             |                         | hyphenate                     |
|                             | Machine Learning Model  | spaCy syllable                |
|                             |                         | spaCy nlp (same little faster)|
| **Count Only**              | User Contributed        | basirico                      |
|                             |                         | anonuser1                     |
|                             |                         | abigailb                      |
|                             |                         | hauntninja                    |
|                             |                         | tarun – sylco                 |
|                             | Library                 | nltk (cmudict)                |
|                             |                         | syllapy                       |
|                             |                         | syllables                     |
|                             | Machine Learning Model  | meow25                        |
|                             |                         | bigphoney                     |

**1.4 Results**



### To be implemented:
- Gold standard is dictionary (human intervention)
- Web based approach, apis etc. (https://stackoverflow.com/questions/10414957/using-python-to-find-syllables/10416028#10416028)
     - https://www.howmanysyllables.com/syllables/table
     - https://www.wordcalc.com/index.php
