#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Gestalt Lur.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import sys
import os
import re
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

HTTP_SUB_REGEX = re.compile('(https?://[\S]+)')

EN_WORDS_SUB_REGEX = re.compile('(\w+)')

class Words(db.Model):
    runtime = db.StringProperty()
    word = db.StringProperty()
    count = db.IntegerProperty(default=1 )

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

class AnalyzeTweets(webapp2.RequestHandler):
    """
    if user_name exist, fetch FETCH_TWEET_CNT tweets
    else display no such user
    or that user locked his tweets
    """
    #TODO if it not use DB could be faster, not use it.
    def post(self):

        user_name = self.request.get('username', FETCH_TWEET_CNT )

        tweets_entites = TweetsFetcher.request_timeline.get_tweets( user_name, FETCH_TWEET_CNT )
        
        for tweet in tweets_entites:
            # some traditional Chinese tweet may be detected as japanese
            if (tweet[ 'lang' ] == 'zh') or (tweet[ 'lang' ] == 'jp'):
                #words in tweet_word_list should check to ensure they're all Chinese words, or use regex to remove non-Chinese words
                tweet_text = HTTP_SUB_REGEX.sub( '', tweet[ 'text' ] )
                tweet_text = EN_WORDS_SUB_REGEX.sub( '', tweet[ 'text' ] )
                tweet_word_list = list( jieba.cut( tweet_text ) )

                for w in tweet_word_list:
                    if sys.getsizeof( w ) > 32: # more than two zh char
                        #word_data = Words.get(keys=w)
                        word_data = Words.gql("WHERE word = :1", w).get()
                        #print word_data.__class__
                        if word_data == None:
                            word_data = Words( get_word_key( w ) )
                            word_data.word = w
                        else:
                            word_data.count = word_data.count + 1
                        word_data.put()

        #redirect
        self.redirect('/')

class ShowTweets(webapp2.RequestHandler):
    """
    List fetched tweets, for test use
    not to save in DB
    """
    def post(self):

        user_name = self.request.get('username', FETCH_TWEET_CNT )

        tweets_entites = TweetsFetcher.request_timeline.get_tweets( user_name, FETCH_TWEET_CNT )
        
        template_values = {
            'tweets': tweets_entites,
            'user': user_name
        }

        template = JINJA_ENVIRONMENT.get_template('show_tweet.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage),
                             ('/fetch', AnalyzeTweets ),
                             ('/list', ShowTweets )] , debug=True)

