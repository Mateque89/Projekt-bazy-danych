
from eventHandler import *
import json
import sys



handler = EventHandler()
while True:
    inp = input()
    if input == '':
        exit()
    obj = json.loads(inp)
    handler.Event(obj)

