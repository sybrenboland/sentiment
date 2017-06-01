import os
import codecs
import json
import spacy
import pandas as pd
import itertools as it

from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

nlp = spacy.load('en')


intermediate_directory = os.path.join('.', 'intermediate')
unigram_sentences_filepath = os.path.join(intermediate_directory,
                                          'unigram_sentences_all.txt')

unigram_sentences = LineSentence(unigram_sentences_filepath)

for unigram_sentence in it.islice(unigram_sentences, 230, 240):
    print u' '.join(unigram_sentence)
    print u''

bigram_model_filepath = os.path.join(intermediate_directory, 'bigram_model_all')


if 1 == 1:

    bigram_model = Phrases(unigram_sentences)

    bigram_model.save(bigram_model_filepath)
    
# load the finished model from disk
bigram_model = Phrases.load(bigram_model_filepath)

bigram_sentences_filepath = os.path.join(intermediate_directory,
                                         'bigram_sentences_all.txt')

if 1 == 1:

    with codecs.open(bigram_sentences_filepath, 'w', encoding='utf_8') as f:
        
        for unigram_sentence in unigram_sentences:
            
            bigram_sentence = u' '.join(bigram_model[unigram_sentence])
            
            f.write(bigram_sentence + '\n')








#for bigram_sentence in it.islice(bigram_sentences, 230, 240):
#    print u' '.join(bigram_sentence)
#    print u''






