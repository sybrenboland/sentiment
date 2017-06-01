import os
from gensim.models.ldamulticore import LdaMulticore

intermediate_directory = os.path.join('..', 'intermediate')
lda_model_filepath = os.path.join(intermediate_directory, 'lda_model_all')
lda = LdaMulticore.load(lda_model_filepath)

import spacy
from gensim.models import Phrases
from gensim.corpora import Dictionary

nlp = spacy.load('en')

bigram_model_filepath = os.path.join(intermediate_directory, 'bigram_model_all')
bigram_model = Phrases.load(bigram_model_filepath)

trigram_model_filepath = os.path.join(intermediate_directory,
                                      'trigram_model_all')
trigram_model = Phrases.load(trigram_model_filepath)

trigram_dictionary_filepath = os.path.join(intermediate_directory,
                                           'trigram_dict_all.dict')
trigram_dictionary = Dictionary.load(trigram_dictionary_filepath)


def topicToString(topics):
    topics_plus = []
    
    for key in topics.keys():
        topics_plus.append(str(key) + " " + topic_names[key])
    
    return topics_plus


def createTopicDictionary(tweets, topics):
    topicDict = {}
    
    for tweet in tweets:
        topic = mostRelevantTopic(tweet)
        
        if(topic in topicToString(topics)):
            if(topicDict.has_key(topic)):
                topicDict[topic] = topicDict[topic] + 1
            else:
                topicDict.update({topic:0})
    
    return topicDict


def lda_description(review_text, min_topic_freq=0.05):
    
    # parse the review text with spaCy
    parsed_review = nlp(review_text)
    
    # lemmatize the text and remove punctuation and whitespace
    unigram_review = [token.lemma_ for token in parsed_review
                      if not (token.is_punct or token.is_space)]
    
    # apply the first-order and secord-order phrase models
    bigram_review = bigram_model[unigram_review]
    trigram_review = trigram_model[bigram_review]
    
    # remove any remaining stopwords
    trigram_review = [term for term in trigram_review
                      if not nlp.vocab[unicode(term)].is_stop]
    
    # create a bag-of-words representation
    review_bow = trigram_dictionary.doc2bow(trigram_review)
    
    # create an LDA representation
    review_lda = lda[review_bow]
    
    # sort with the most highly related topics first
    review_lda = sorted(review_lda, key=lambda (topic_number, freq): -freq)
    
    topics = []
    for topic_number, freq in review_lda:
        if freq < min_topic_freq:
            break
            
        # print the most highly related topic names and frequencies
        topics.append([topic_number,topic_names[topic_number], round(freq, 3)])
    
    return topics


def mostRelevantTopic(tweet):
    topics = lda_description(tweet)

    if not topics:
        return "Unknown"
    else:
        return str(topics[0][0]) + " " + topics[0][1]

topic_names = {0: u'',
               1: u'indian',
               2: u'online',
               3: u'',
               4: u'bbq',
               5: u'salad',
               6: u'price',
               7: u'french (language)',
               8: u'buffet',
               9: u'',
               10: u'great food',
               11: u'',
               12: u'',
               13: u'service',
               14: u'',
               15: u'german (language)',
               16: u'',
               17: u'',
               18: u'great experience',
               19: u'location',
               20: u'',
               21: u'',
               22: u'bar & drinks',
               23: u'',
               24: u'vegetarian & vegan',
               25: u'',
               26: u'',
               27: u'',
               28: u'thai food',
               29: u'deep frie',
               30: u'bad experience',
               31: u'sushi',
               32: u'',
               33: u'breakfast',
               34: u'in the past',
               35: u'decor',
               36: u'',
               37: u'',
               38: u'',
               39: u'food taste',
               40: u'mexican food',
               41: u'coffee & dessert',
               42: u'german (language)',
               43: u'pizza',
               44: u'sandwich',
               45: u'ambiance',
               46: u'Vegas',
               47: u'',
               48: u'lunch',
               49: u''}
