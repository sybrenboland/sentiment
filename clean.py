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
trigram_reviews_filepath = os.path.join(intermediate_directory,
                                        'trigram_transformed_reviews_all.txt')

review_txt_filepath = os.path.join(intermediate_directory,
                                   'review_text_all.txt')

def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """
    
    return token.is_punct or token.is_space

def line_review(filename):
    """
    generator function to read in reviews from the file
    and un-escape the original line breaks in the text
    """
    
    with codecs.open(filename, encoding='utf_8') as f:
        for review in f:
            yield review.replace('\\n', '\n')
            
def lemmatized_sentence_corpus(filename):
    """
    generator function to use spaCy to parse reviews,
    lemmatize the text, and yield sentences
    """
    
    for parsed_review in nlp.pipe(line_review(filename),
                                  batch_size=10000, n_threads=4):
        
        for sent in parsed_review.sents:
            yield u' '.join([token.lemma_ for token in sent
                             if not punct_space(token)])
            

bigram_model_filepath = os.path.join(intermediate_directory, 'bigram_model_all')
bigram_model = Phrases.load(bigram_model_filepath)

trigram_model_filepath = os.path.join(intermediate_directory,
                                      'trigram_model_all')
trigram_model = Phrases.load(trigram_model_filepath)

if 1 == 1:

    with codecs.open(trigram_reviews_filepath, 'w', encoding='utf_8') as f:
        
        for parsed_review in nlp.pipe(line_review(review_txt_filepath),
                                      batch_size=10000, n_threads=8):
            
            # lemmatize the text, removing punctuation and whitespace
            unigram_review = [token.lemma_ for token in parsed_review
                              if not punct_space(token)]
            
            # apply the first-order and second-order phrase models
            bigram_review = bigram_model[unigram_review]
            trigram_review = trigram_model[bigram_review]
            
            # remove any remaining stopwords
            trigram_review = [term for term in trigram_review
                              if not nlp.vocab[unicode(term)].is_stop]
            
            # write the transformed review as a line in the new file
            trigram_review = u' '.join(trigram_review)
            f.write(trigram_review + '\n')

print u'Original:' + u'\n'

#for review in it.islice(line_review(review_txt_filepath), 11, 12):
 #   print review

#print u'----' + u'\n'
#print u'Transformed:' + u'\n'

#with codecs.open(trigram_reviews_filepath, encoding='utf_8') as f:
#    for review in it.islice(f, 11, 12):
#        print review