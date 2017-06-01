from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore

import pyLDAvis
import pyLDAvis.gensim
import warnings
import cPickle as pickle
import os

from gensim.models import Phrases
from gensim.models.word2vec import LineSentence


intermediate_directory = os.path.join('.', 'intermediate')


trigram_sentences_filepath = os.path.join(intermediate_directory,
                                          'trigram_sentences_all.txt')

from gensim.models import Word2Vec

trigram_sentences = LineSentence(trigram_sentences_filepath)
word2vec_filepath = os.path.join(intermediate_directory, 'word2vec_model_all')

if 1 == 1:

    # initiate the model and perform the first epoch of training
    food2vec = Word2Vec(trigram_sentences, size=100, window=5,
                        min_count=20, sg=1, workers=7)
    
    food2vec.save(word2vec_filepath)
             
    # perform another 11 epochs of training
    for i in range(1,12):

        food2vec.train(trigram_sentences)
        food2vec.save(word2vec_filepath)
        
# load the finished model from disk
food2vec = Word2Vec.load(word2vec_filepath)
food2vec.init_sims()

print u'{} training epochs so far.'.format(food2vec.train_count)