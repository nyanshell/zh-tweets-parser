import httplib
import os

from obtain_oauth import obtain_bearer_token 
from gzip_decode import gzip_decode

def get_tweets( user_name, cnt_num ):

    #read consumer_key and consumer_secret from oauth_key.txt
    _curpath = os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
    abs_path = os.path.join( _curpath, 'oauth_key.txt')
    key_file = open( abs_path, 'rb' )
    consumer_key = key_file.readline().replace( '\n', '' )
    consumer_secret = key_file.readline().replace( '\n', '' )
    key_file.close()

    #try:
    access_token = obtain_bearer_token( consumer_key, consumer_secret )
    #except Exception as e:
    #    print e.value
        #TODO raise a GetTweetError here
    host = 'api.twitter.com'
    url = '/1.1/statuses/user_timeline.json?count=' + str(cnt_num) + '&screen_name=' + user_name

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", "Bearer %s" % access_token )   
    #connect.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    #connect.putheader("Content-Length", "%d" % len( msg ))
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()
    print twitter_response.status

    zipped_tweets = twitter_response.read()

    tweets_entites = gzip_decode( zipped_tweets )

    connect.close()
    
    return tweets_entites
