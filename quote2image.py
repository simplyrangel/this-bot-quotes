"""Takes a string and saves it as an image.
https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html

Recommended Twitter timeline image size: 1024x512
https://www.mainstreethost.com/blog/social-media-image-size-cheat-sheet/
"""
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import helper

# recommended image size:
twitterx = 1024
twittery = 512

# border size:
borderx = 80
bordery = 40

# anchor the text to the border's top-left corner:
text_anchor = (borderx, bordery)

# define textbox pixel length:
boxx = twitterx - 2*borderx

# read quotes:
df = pd.read_csv("bookquotes.csv")
df = df.fillna("unknown")
for ii in df.index:
    quote = df.loc[ii, "quote"]
    book = df.loc[ii,"title"]
    auth = df.loc[ii, "author"]

    # add actual quotes around the quote and the book attribute:
    quote = '"%s"'%quote
    if book!="unknown":
       book = "'%s'"%book

    # create intermediate image, font, and drawn quote:
    # this intermediate image will be used to calculate the correct
    # y-length in pixels: 
    imi = Image.new("RGB", (twitterx,twittery), "white")
    fnt = ImageFont.truetype("Pillow/Tests/fonts/Norasi.ttf", 40)
    di = ImageDraw.Draw(imi)

    # create new quote:
    result, boxy = helper.format_text(
        quote, 
        book,
        auth,
        di, 
        fnt, 
        boxx)
        
    # close intermediate image and create one with the new boxy:
    imi.close()
    boxy = boxy+2*bordery
    im = Image.new("RGB", (twitterx,boxy),"white")
    d = ImageDraw.Draw(im)
    
    # write formatted text to image:
    d.text(text_anchor, result, font=fnt, fill=(0,0,0))

    # create text
    im.save("bin/testimage_%d.png" %ii)
    im.close()


