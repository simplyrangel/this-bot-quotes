"""A simple Twitter API wrapper. Uses twurl, a Twitter bash 
tool. See more info at: https://github.com/twitter/twurl
"""
from subprocess import Popen, PIPE
import json
import helper.twapi as twapi

def upload_media(fi):
    cmd = [
        "twurl",
        "-H", #specify host
        "upload.twitter.com",
        "-X", #specify request method
        "POST",
        twapi.MEDIA_UPLOAD,
        "--file",
        fi,
        "--file-field",
        "media"]
    process = Popen(cmd,stdout=PIPE,stderr=PIPE)
    stdout,stderr=process.communicate()
    return json.loads(stdout)
        
def tweetme(text,media_id=None):
    if media_id is None:
        cmd = [
            "twurl", 
            twapi.STATUS_UPDATE,
            "-d", #sends specified data in a POST request
            "status=%s" %text]
    else:
        cmd = [
            "twurl",
            twapi.STATUS_UPDATE,
            "-d", #sends specified data in a POST request
            "media_ids=%s&status=%s" %(media_id,text)]
    process = Popen(cmd,stdout=PIPE,stderr=PIPE)
    stdout,stderr = process.communicate()

def generate_tweet(auth, book, quote, topics=None, char_limit=280):
    tags = generate_hashtags(auth,book,topics)
    
    # leave 2 characters for newline between quote and hashtags
    # leave 3 characters for ellipses if quote is truncated
    # leave 1 character for trailing quotation if quote is truncated
    if len(tags) + len(quote) + 2 <= 280:
        return "%s\n%s" %(quote,tags)
    else:
        char_offset = 6
        quote_chars = char_limit - len(tags) - char_offset
        return "%s...'\n%s" %(quote[:quote_chars],tags)

def generate_hashtags(auth, book, topics=None):
    if book!="unknown":
        tweet_text = "#{author} #{book} #bookquotes #books".format(
            book=_format_hashtag(book),
            author=_format_hashtag(auth))
    else:
        tweet_text = "#{author} #bookquotes #books".format(
            author=_format_hashtag(auth))
    if type(topics) is str:
        l = ["#%s " %x for x in topics.replace(" ","").split(";")]
        s = "".join(l)
        tweet_text = "%s %s" %(tweet_text,s)
    
    # return tweet text:
    return tweet_text

def _format_hashtag(text):
    return text.replace(
        " ","").replace(
        ",","").replace(
        ".","").replace(
        "'","").replace( #straight quote
        "’","").replace( #curly quote
        "(","").replace(
        ")","").replace(
        ":","").replace(
        "-","").replace(
        "&","")

def get_last_tweet(count=1):
    process = Popen(
        ["twurl",
        "/1.1/statuses/user_timeline.json?count=%d" %count],
        stdout=PIPE,
        stderr=PIPE)
    stdout,sterr = process.communicate()
    return json.loads(stdout)

def get_timeline():
    process = Popen( #default request method is GET
        ["twurl", 
        twapi.HOME_TIMELINE],
        stdout=PIPE,
        stderr=PIPE)
    stdout, stderr = process.communicate()
    return json.loads(stdout)    
    
    
