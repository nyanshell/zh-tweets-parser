baklava-zh-tweet-parser
=========

A Chinese tweets parser web app, use [Jieba] for word segmentation.

Running on GAE.

Main functions
-------------
  - input username and find out the words that most frequently used in 
  
  user's tweets.


Deploy
------
  1. Download code

  2. Add your tweet API consumer key & consumer secret to 
  
  TweetsFetcher/oauth_key.txt( in separate lines )
  
  3. Create an application on GAE, [upload application use appcfg.py] 
  
  4. Done

Issues
------
  - Fatal Error: Memory Limit Exceeded on GAE while request

TODO-LIST
---------
  - Fix MLE error

Changelog
---------
  - 24/05/2013 upload refactor code, unfork from Jieba, turned into 
  a "normal" repository( Because it will never merge back ).
  
  - 23/05/2013 disable temporary file( GAE not support )

version
-------
  - incomplete currently
    
[Jieba]: https://github.com/fxsjy/jieba
[upload application use appcfg.py]: https://developers.google.com/appengine/docs/python/gettingstartedpython27/uploading
