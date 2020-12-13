"""A module to create images from quote texts. Uses the Pillow
library for image creation:
https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html

Recommended Twitter timeline image size:1024x512
https://www.mainstreethost.com/blog/social-media-image-size-cheat-sheet/
"""
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def imake(auth,book,quote,poetry_flag,**kwargs):
    if poetry_flag is True:
        poetry2image(auth,book,quote,**kwargs)
    else:
        quote2image(auth,book,quote,**kwargs)

def poetry2image(
        auth,
        book,
        quote,
        imagec="white",
        textc = "black",
        borderx=80,
        bordery=40,
        text_anchor="default",
        font="Pillow/Tests/fonts/Norasi.ttf",
        fontsize=40,
        outfi="bin/quote_of_day.png",
        ):
    # anchor text to border's top-left corner:
    if text_anchor=="default":
        text_anchor = (borderx, bordery)
    
    # determine the number of characters in the 
    # longest line of poetry:
    quote_lines = quote.split("\n")
    max_line_chars = max([len(x) for x in quote_lines])

    # format book title to fit the box:
    boxbook = _boxit(book, max_line_chars)
    
    # add the author and book attribute:
    result = """%s\n\n-%s\n%s""" %(quote,auth,boxbook)
    
    # create intermediate image, font, and drawn quote:
    # this intermediate image will be used to calculate the correct
    # x-length and y-length in pixels: 
    imi = Image.new("RGB", (1024,512), imagec)
    fnt = ImageFont.truetype(font, fontsize)
    di = ImageDraw.Draw(imi)
    
    # calculate box and image y-length in pixels:
    boxx = di.textsize(result,font=fnt)[0]
    boxy = di.textsize(result,font=fnt)[1]

    # close intermediate image and create one with the new boxy:
    imi.close()
    imagex = boxx+2*borderx
    imagey = boxy+2*bordery
    im = Image.new("RGB", (imagex,imagey),imagec)
    d = ImageDraw.Draw(im)

    # write formatted text to image:
    d.text(text_anchor, result, font=fnt, fill=textc)

    # create text
    im.save(outfi)
    im.close()

def quote2image(
        auth,
        book,
        quote,
        imagec = "white",
        textc = "black",
        imagex=1024, #pixels
        borderx=80, #pixels
        bordery=40, #pixels
        text_anchor="default",
        font="Pillow/Tests/fonts/Norasi.ttf",
        fontsize=40,
        outfi = "bin/quote_of_day.png",
        ):
    # anchor text to border's top-left corner:
    if text_anchor=="default":
        text_anchor = (borderx,bordery)
    
    # define textbox pixel length:
    boxx = imagex - 2*borderx
    
    # create intermediate image, font, and drawn quote:
    # this intermediate image will be used to calculate the correct
    # y-length in pixels: 
    imi = Image.new("RGB", (imagex,512), imagec)
    fnt = ImageFont.truetype(font, fontsize)
    di = ImageDraw.Draw(imi)
    
    # format quote text:
    result, boxy = format_text(
        quote, 
        book,
        auth,
        di, 
        fnt, 
        boxx)

    # close intermediate image and create one with the new boxy:
    imi.close()
    imagey = boxy+2*bordery
    im = Image.new("RGB", (imagex,imagey),imagec)
    d = ImageDraw.Draw(im)

    # write formatted text to image:
    d.text(text_anchor, result, font=fnt, fill=textc)

    # create text
    im.save(outfi)
    im.close()
    
def format_text(
        text, #string
        book, #string
        author, #string
        d, #image object
        font, #font object
        boxx #text box x length [pixels]
        ):
    # format a text string until the shape fits inside the provided 
    # textbox dimensions.
    #
    # get text pixel length:
    text_pixel_length = d.textsize(text, font=font)[0]
    
    # find number of characters that correspond to the textbox x-size:
    # create long string to use:
    astring = "".join(["a" for x in range(100)])
    for pointer in range(len(astring)):
        pointer_pixels = d.textsize(astring[:pointer], font=font)[0]
        boxx_char_length = pointer
        if pointer_pixels >= boxx:
            break
    
    # format quote and book title to fit the box:
    boxquote = _boxit(text, boxx_char_length)
    boxbook = _boxit(book, boxx_char_length)
    
    # add the author and book attribute:
    result = """%s\n\n-%s\n%s""" %(boxquote,author,boxbook)
    
    # calculate box y-length in pixels:
    boxy = d.textsize(result,font=font)[1]
    
    # return formatted quote:
    return(result,boxy)

def _boxit(astring, boxx_char_length):
    ls = list(astring)
    pointer = boxx_char_length
    while pointer < len(astring):
        if ls[pointer].isspace() is True:
            ls[pointer] = "\n"
        else:
            pointer -= (boxx_char_length + 1)
        pointer += boxx_char_length
    return "".join(ls)







