"""A module of helpful functions."""
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def format_text(
        text, #string
        book, #string
        author, #string
        d, #image object
        font, #font object
        boxx, #text box x length [pixels]
        boxy_min=None #minimum text box y length [pixels]
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
    
    # return formatted quote:
    return(result)

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







