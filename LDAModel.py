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
trigram_dictionary_filepath = os.path.join(intermediate_directory,
                                           'trigram_dict_all.dict')
trigram_reviews_filepath = os.path.join(intermediate_directory,
                                        'trigram_transformed_reviews_all.txt')


# this is a bit time consuming - make the if statement True
# if you want to learn the dictionary yourself.
if 0 == 1:

    trigram_reviews = LineSentence(trigram_reviews_filepath)

    # learn the dictionary by iterating over all of the reviews
    trigram_dictionary = Dictionary(trigram_reviews)
    
    # filter tokens that are very rare or too common from
    # the dictionary (filter_extremes) and reassign integer ids (compactify)
    trigram_dictionary.filter_extremes(no_below=10, no_above=0.4)
    trigram_dictionary.compactify()

    trigram_dictionary.save(trigram_dictionary_filepath)
    
# load the finished dictionary from disk

trigram_dictionary = Dictionary.load(trigram_dictionary_filepath)
 
trigram_bow_filepath = os.path.join(intermediate_directory,
                                    'trigram_bow_corpus_all.mm')
 
def trigram_bow_generator(filepath):
    """
    generator function to read reviews from a file
    and yield a bag-of-words representation
    """
     
    for review in LineSentence(filepath):
        yield trigram_dictionary.doc2bow(review)


# this is a bit time consuming - make the if statement True
# if you want to build the bag-of-words corpus yourself.

if 0 == 1:
 
    # generate bag-of-words representations for
    # all reviews and save them as a matrix
    MmCorpus.serialize(trigram_bow_filepath,
                       trigram_bow_generator(trigram_reviews_filepath))
     
# load the finished bag-of-words corpus from disk
trigram_bow_corpus = MmCorpus(trigram_bow_filepath)
 
 
lda_model_filepath = os.path.join(intermediate_directory, 'lda_model_all')


# this is a bit time consuming - make the if statement True
# if you want to train the LDA model yourself.

if 0 == 1:
 
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
         
        # workers => sets the parallelism, and should be
        # set to your number of physical cores minus one
        lda = LdaMulticore(trigram_bow_corpus,
                           num_topics=50,
                           id2word=trigram_dictionary,
                           workers=7)
     
    lda.save(lda_model_filepath)
     
# load the finished LDA model from disk
lda = LdaMulticore.load(lda_model_filepath)


LDAvis_data_filepath = os.path.join(intermediate_directory, 'ldavis_prepared')


if 1 == 1:

    LDAvis_prepared = pyLDAvis.gensim.prepare(lda, trigram_bow_corpus,
                                              trigram_dictionary)

    with open(LDAvis_data_filepath, 'w') as f:
        pickle.dump(LDAvis_prepared, f)
        
# load the pre-prepared pyLDAvis data from disk
with open(LDAvis_data_filepath) as f:
    LDAvis_prepared = pickle.load(f)







