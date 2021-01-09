"""Create the social media preview. Might as well use a short, engaging
quote. Let's do a black background with white text for affect.

Github recommends social media preview images should be at least 
640x320px, and 1280x640px for best display.
"""
import numpy as np
import pandas as pd
import helper.images as images

# read quotes data:
# Let's use Victor Hugo's famous 'Hunchback' quote,
# or Thrity Umrigar's quote on freedom:
df = pd.read_csv("bookquotes.csv", comment="#")
quote_id = 1 #32=Hunchback; 1=Thrity
auth = df.loc[quote_id,"author"]
book = df.loc[quote_id,"title"]
quote = df.loc[quote_id, "quote"]
poetry_flag = df.loc[quote_id, "poetry"]
quote = "'%s'" %quote
book="'%s'" %book

# create image:
images.imake(
    auth,
    book,
    quote,
    imagec="black",
    textc="white",
    poetry_flag=poetry_flag,
    borderx=180,
    outfi="bin/0-social-media-preview.png")
