import tweepy
import codecs

import config

consumer_key= 'mtlMtiqBS9nxPpQAWqRr8Uidp'
consumer_secret= 'V495bL2l8ARcJ79pmC7uc71KjU2UqGokiObGV7J8aWnnIYZHOt'

access_token='837579226320678912-tOU86ocpLGISf4ZTcHL7TGQSmFxQbnt'
access_token_secret='aLQEQvR7RYcVJcWwP6wRrh92ZxKLOcxEWfc1cbBDylwJM'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


import json
from tweepy import Stream
from tweepy.streaming import StreamListener

tweetsStream = codecs.open('tweets/tweets.txt', 'w', encoding='utf-8')

class Listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        tweetsStream.write(tweet['text'] + '\n ###' )
        return True

    def on_error(self, status):
        print status


l = Listener()
stream = Stream(auth, l)

#This line filter Twitter Streams to capture data by the keywords: 
stream.filter(track=config.searchWords)

import sched, time
s = sched.scheduler(time.time, time.sleep)
