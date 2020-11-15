"""Tweet quote images with hashtags in perpetuity (as long as terminal
is open)."""
import numpy as np
import pandas as pd
import threading
import time
import helper.tweetwrapper as twrap
import helper.images as images

# ----------------------------------------------------
# Local functions.
# ----------------------------------------------------
def console_message(text):
    print("""On {time} I tweeted:\n{tweet}\n""".format(
        time=time.ctime(),
        tweet=text))

def tweet_quote():
    # read quotes data:
    df = pd.read_csv("bookquotes.csv")
    df = df.fillna("unknown")

    # choose a random quote:
    rand_id = np.random.randint(df.index[0], df.index[-1]+1)
    auth = df.loc[rand_id,"author"]
    book = df.loc[rand_id,"title"]
    quote = df.loc[rand_id, "quote"]

    # add quotes around the quote text and book text:
    quote = "'%s'" %quote
    if book!="unknown":
        book="'%s'" %book

    # create tweet hashtags:
    tweet_text = twrap.generate_hashtags(auth, book)

    # create tweet image:
    tweet_image_text = images.quote2image(auth,book,quote)

    # upload tweet image:
    upload_stdout = twrap.upload_media("bin/quote_of_day.png")
    media_id = upload_stdout["media_id"]

    # tweet the quote:
    twrap.tweetme(tweet_text,media_id=media_id)
    
    # print to console:
    console_message(tweet_image_text)
    
# ----------------------------------------------------
# Execute command.
# ----------------------------------------------------
# define interval:
interval_hours = 2 #every two hours
interval_seconds = interval_hours*60*60

# create event and execute once every interval:
ticker = threading.Event()
while ticker.wait(interval_seconds) is False:
    tweet_quote()






