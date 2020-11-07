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
imagex = 1024
imagey = 512
twitter_timeline_size = (imagex, imagey) #pixels
borderx = 100
bordery = 100
text_anchor = (borderx, bordery)

# define textbox shape:
boxx = imagex - 2*borderx
boxy = imagey - 2*bordery

# read quotes:
df = pd.read_csv("bookquotes.csv")
for ii in range(10):
    quote = df.loc[ii, "quote"]
    book = df.loc[ii,"title"]
    auth = df.loc[ii, "author"]

    # add actual quotes around the quote and the book attribute:
    quote = '"%s"'%quote
    book = "'%s'"%book

    # create image. 
    im = Image.new("RGB", twitter_timeline_size, "white")

    # get a font:
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)

    # draw the quote:
    d = ImageDraw.Draw(im)

    # create new quote:
    new_quote = helper.format_text(
        quote, 
        book,
        auth,
        d, 
        fnt, 
        boxx)
    print(new_quote)

    d.text(text_anchor, new_quote, font=fnt, fill=(0,0,0))

    # create text
    im.save("bin/testimage_%d.png" %ii)
    im.close()


