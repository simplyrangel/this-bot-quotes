"""A wrapper for all things Twitter."""
from subprocess import Popen, PIPE
import json
import helper.twapi as twapi

def get_timeline():
    process = Popen(
        ["twurl", 
        twapi.HOME_TIMELINE],
        stdout=PIPE,
        stderr=PIPE)
    stdout, stderr = process.communicate()
    return json.loads(stdout)
