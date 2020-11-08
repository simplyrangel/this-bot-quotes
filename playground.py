"""Playground for testing code."""
import helper.tweetwrapper as twrap
timeline = twrap.get_timeline()
tweet = timeline[0]
print(tweet["text"])
