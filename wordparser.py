# -*- coding: utf-8 -*-
import jinja2
import sys
import os
import cgi
import datetime
import urllib
import webapp2
import jieba
import TweetsFetcher.request_timeline
#from TweetsFetcher.request_timeline import get_tweets  
from google.appengine.ext import db

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

FETCH_TWEET_CNT = 5

FETCH_WORD_RANK_CNT = 10

class Words(db.Model):
    word = db.StringProperty()
    count = db.IntegerProperty(default=0 )

def get_word_key(word_key=None):
    return db.Key().from_path('Words', word_key)

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        wordfrq_query = Words.all().order('-count')
        words = wordfrq_query.fetch( FETCH_WORD_RANK_CNT )

        template_values = {
            'words': words,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class FetchTweets(webapp2.RequestHandler):
    """
    if user_name exist, fetch FETCH_TWEET_CNT tweets
    else display no such user
    or that user locked his tweets
    """
    def post(self):

        user_name = self.request.get('username', FETCH_TWEET_CNT )

        tweets_entites = TweetsFetcher.request_timeline.get_tweets( user_name, FETCH_TWEET_CNT )
        
        for tweet in tweets_entites:
            tweet_word_list = list( jieba.cut( tweet[ 'text' ] ) )
            #words in tweet_word_list should check to ensure they're all Chinese words
            for w in tweet_word_list:
                if sys.getsizeof( w ) > 32: # more than two zh char
                    #word_data = Words.get(keys=w)
                    word_data = Words.gql("WHERE word = :1", w).get()
                    print word_data.__class__
                    if word_data == None:
                        word_data = Words( get_word_key( w ) )
                        word_data.word = w
                    else:
                        word_data.count = word_data.count + 1
                    word_data.put()

        #redirect
        self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage), ('/fetch', FetchTweets)] , debug=True)

