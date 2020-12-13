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
     
def generate_hashtags(auth, book, topics=None):
    if book!="unknown":
        tweet_text = "#{author} #{book} #bookquotes #reading".format(
            book=_format_hashtag(book),
            author=_format_hashtag(auth))
    else:
        tweet_text = "#{author} #bookquotes #reading".format(
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
    
    
