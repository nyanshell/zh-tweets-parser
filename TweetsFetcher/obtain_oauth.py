"""
get application-only oauth bearer
date : 2013-05-21
author : Gestalt Lur
"""
import httplib, base64
import urllib
import gzip
import StringIO
import ast

from gzip_decode import gzip_decode
"""
according to this document, consumer key &
consumer secret were not change after encoding
to url, but this may change in future.
https://dev.twitter.com/docs/auth/application-only-auth
"""

def obtain_bearer_token( consumer_key, consumer_secret ):
    # use for test base64 encoding
    #consumer_key = b'xvz1evFS4wEEPTGEFPHBog'
    #consumer_secret = b'L8qq9PZyRg6ieKGEKhZolGC0vJWLw8iEJ88DRdyOg'
    
    host = "api.twitter.com"
    url = "/oauth2/token"

    # POST request to obtain bearer token
    encoded_bearer = base64.b64encode( '%s:%s' % (consumer_key, consumer_secret)) 

    twitter_conn = httplib.HTTPSConnection( host )

    msg = r'grant_type=client_credentials'
    #msg = urllib.urlencode({'grant_type' : 'client_credentials'})
    #write headers
    twitter_conn.putrequest("POST", url )
    twitter_conn.putheader("Host", host )
    twitter_conn.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    twitter_conn.putheader("Authorization", "Basic %s" % encoded_bearer )   
    twitter_conn.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    twitter_conn.putheader("Content-Length", "%d" % len( msg ))
    twitter_conn.putheader("Accept-Encoding", "gzip" )
    twitter_conn.endheaders( message_body=msg )
    #twitter_conn.send( msg )

    twitter_response = twitter_conn.getresponse()

    # Check that everything went ok.
    if twitter_response.status != 200:
        #raise BearerGetException("Failed to request tweets, code " + str(twitter_response.status))
        print "Failed to request tweets, code " + str(twitter_response.status)
        return "Failed to request tweets, code " + str(twitter_response.status)

    # Read the response.
    # currently it will return .json file
    raw_data = twitter_response.read()
    respond_body_dict = gzip_decode( raw_data )

    #header_dict = twitter_response.getheaders()

    twitter_conn.close()

    return respond_body_dict['access_token']
