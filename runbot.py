"""Tweet quote images with hashtags in perpetuity (as long as terminal
is open)."""
import numpy as np
import pandas as pd
import threading
from datetime import datetime
import helper.tweetwrapper as twrap
import helper.images as images

# ----------------------------------------------------
# Local functions.
# ----------------------------------------------------
def new_id(df,track_id):
    return_flag = False
    while return_flag is False:
        quote_id = np.random.randint(df.index[0], df.index[-1]+1)
        if quote_id not in track_id[-10:]:
            return_flag = True
    return quote_id

def console_message(text):
    print("""{time}: I tweeted:\n{tweet}\n""".format(
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tweet=text))

def tweet_quote(track_id):
    # read quotes data:
    df = pd.read_csv("bookquotes.csv", comment="#")
    df.loc[:,"title"] = df.title.fillna("unknown")
    df.loc[:,"author"] = df.author.fillna("unknown")

    # choose a quote that fits the conditions present
    # in new_id():
    quote_id = new_id(df,track_id)
    auth = df.loc[quote_id,"author"]
    book = df.loc[quote_id,"title"]
    quote = df.loc[quote_id, "quote"]
    topics = df.loc[quote_id, "topics"]
    poetry_flag = df.loc[quote_id, "poetry"]

    # add quotes around the quote text and book text:
    quote = "'%s'" %quote
    if book!="unknown":
        book="'%s'" %book

    # create tweet hashtags:
    tweet_text = twrap.generate_hashtags(auth, book, topics)

    # create tweet image:
    images.imake(
        auth,
        book,
        quote,
        poetry_flag=poetry_flag)

    # upload tweet image:
    upload_stdout = twrap.upload_media("bin/quote_of_day.png")
    media_id = upload_stdout["media_id"]

    # tweet the quote:
    twrap.tweetme(tweet_text,media_id=media_id)
    
    # print to console:
    console_message(quote)
    
    # track the quote id:
    track_id.append(quote_id)
    
# ----------------------------------------------------
# Execute command.
# ----------------------------------------------------
# define interval:
interval_hours = 1
interval_seconds = interval_hours*60*60

# define hours when the bot can tweet:
hi = 7 #first hour; 7am
he = 22 #last hour; 10pm

# track previous quotes to reduce repeats:
df = pd.read_csv("bookquotes.csv", comment="#")
track_id = []

# create event and execute once every interval:
ticker = threading.Event()
while ticker.wait(interval_seconds) is False:
    now = datetime.now()
    ti = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=hi)
    te = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=he)
    if now >= ti and now <= te:
        tweet_quote(track_id)
    else:
        print("no tweet; outside acceptable time.")






