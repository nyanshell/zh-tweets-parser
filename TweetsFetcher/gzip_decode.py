"""
decode gzip encoded json
"""
import gzip
import StringIO
import ast
import json

def gzip_decode( raw_data ):

    raw_stream = StringIO.StringIO( raw_data ) 
    gzip_obj = gzip.GzipFile( fileobj=raw_stream )

    decoded_str = gzip_obj.read()
    #print json.__class__
    try:
        json_dict = ast.literal_eval( decoded_str )
        return json_dict
    #if ValueError occured, it must be more than one tweets/.json entity
    except ValueError:
        json_list = json.loads( decoded_str )
        return json_list
    finally:
        raw_stream.close()
