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
def console_message(text):
    print("""{time}: I tweeted:\n{tweet}\n""".format(
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tweet=text))

def tweet_quote():
    # read quotes data:
    df = pd.read_csv("bookquotes.csv", comment="#")
    df.loc[:,"title"] = df.title.fillna("unknown")
    df.loc[:,"author"] = df.author.fillna("unknown")

    # choose a random quote:
    rand_id = np.random.randint(df.index[0], df.index[-1]+1)
    auth = df.loc[rand_id,"author"]
    book = df.loc[rand_id,"title"]
    quote = df.loc[rand_id, "quote"]
    poetry_flag = df.loc[rand_id, "poetry"]

    # add quotes around the quote text and book text:
    quote = "'%s'" %quote
    if book!="unknown":
        book="'%s'" %book

    # create tweet hashtags:
    tweet_text = twrap.generate_hashtags(auth, book)

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
    
# ----------------------------------------------------
# Execute command.
# ----------------------------------------------------
# define interval:
interval_hours = 2 #every two hours
interval_seconds = interval_hours*60*60

# define hours when the bot can tweet:
hi = 7 #first hour; 7am
he = 22 #last hour; 10pm

# create event and execute once every interval:
ticker = threading.Event()
while ticker.wait(interval_seconds) is False:
    now = datetime.now()
    today = datetime.today()
    ti = datetime(
        year=today.year,
        month=today.month,
        day=today.day,
        hour=hi)
    te = datetime(
        year=today.year,
        month=today.month,
        day=today.day,
        hour=he)
    if now >= ti and now <= te:
        tweet_quote()
    else:
        print("no tweet; outside acceptable time.")






