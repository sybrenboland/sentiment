
import os
import codecs
import json
import spacy
import pandas as pd
import itertools as it

from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

intermediate_directory = os.path.join('.', 'intermediate')
trigram_model_filepath = os.path.join(intermediate_directory,
                                      'trigram_model_all')


bigram_sentences_filepath = os.path.join(intermediate_directory,
                                         'bigram_sentences_all.txt')
bigram_sentences = LineSentence(bigram_sentences_filepath)

# this is a bit time consuming - make the if statement True
# if you want to execute modeling yourself.
if 1 == 1:

    trigram_model = Phrases(bigram_sentences)

    trigram_model.save(trigram_model_filepath)
    
# load the finished model from disk
trigram_model = Phrases.load(trigram_model_filepath)


trigram_sentences_filepath = os.path.join(intermediate_directory,
                                          'trigram_sentences_all.txt')


if 1 == 1:

    with codecs.open(trigram_sentences_filepath, 'w', encoding='utf_8') as f:
        
        for bigram_sentence in bigram_sentences:
            
            trigram_sentence = u' '.join(trigram_model[bigram_sentence])
            
            f.write(trigram_sentence + '\n')

trigram_sentences = LineSentence(trigram_sentences_filepath)

for trigram_sentence in it.islice(trigram_sentences, 230, 240):
    print u' '.join(trigram_sentence)
    print u''        

