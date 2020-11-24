"""Create images of all the quotes to see how they appear."""
import numpy as np
import pandas as pd
import helper.tweetwrapper as twrap
import helper.images as images

# read quotes data:
df = pd.read_csv("bookquotes.csv", comment="#")
df.loc[:,"title"] = df.title.fillna("unknown")
df.loc[:,"author"] = df.author.fillna("unknown")

# create images for all the quotes:
for quote_id in df.index:
    auth = df.loc[quote_id,"author"]
    book = df.loc[quote_id,"title"]
    quote = df.loc[quote_id, "quote"]
    poetry_flag = df.loc[quote_id, "poetry"]

    # add quotes around the quote text and book text:
    quote = "'%s'" %quote
    if book!="unknown":
        book="'%s'" %book

    # create tweet image:
    images.imake(
        auth,
        book,
        quote,
        poetry_flag=poetry_flag,
        outfi="bin/sample_image_%d.png" %quote_id)
    
    # show tweet body:
    tweet_text = twrap.generate_hashtags(auth, book)
    print(tweet_text)





