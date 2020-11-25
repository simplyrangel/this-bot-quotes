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
            "-d", 
            "status=%s" %text]
    else:
        cmd = [
            "twurl",
            twapi.STATUS_UPDATE,
            "-d",
            "media_ids=%s&status=%s" %(media_id,text)]
    process = Popen(cmd,stdout=PIPE,stderr=PIPE)
    stdout,stderr = process.communicate()
     
def generate_hashtags(auth, book, topics):
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
    
def get_timeline():
    process = Popen(
        ["twurl", 
        twapi.HOME_TIMELINE],
        stdout=PIPE,
        stderr=PIPE)
    stdout, stderr = process.communicate()
    return json.loads(stdout)    
    
    
