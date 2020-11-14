"""A wrapper for all things Twitter. Uses twurl, a Twitter bash 
tool. See more info at:
https://github.com/twitter/twurl
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
    return stdout
     
def generate_hashtags(auth, book):
    if book!="unknown":
        tweet_text = "#books #bookquotes #{book} #{author}".format(
            book=_format_hashtag(book),
            author=_format_hashtag(auth))
    else:
        tweet_text = "#books #bookquotes #{author}".format(
            author=_format_hashtag(auth))
    return tweet_text

def _format_hashtag(text):
    return text.replace(
        " ","").replace(
        ",","").replace(
        ".","").replace(
        "'","").replace(
        "(","").replace(
        ")","").replace(
        ":","")
    
def get_timeline():
    process = Popen(
        ["twurl", 
        twapi.HOME_TIMELINE],
        stdout=PIPE,
        stderr=PIPE)
    stdout, stderr = process.communicate()
    return json.loads(stdout)    
    
    
