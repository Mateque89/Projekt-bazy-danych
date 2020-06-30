import psycopg2
from eventHandler import EventHandler
import sys
import json




handler = EventHandler()
for line in sys.stdin:
    try:
        if line == '' or line == '\n':
            break
        inp = json.loads(line)
        handler.Event(inp)
    except (Exception) as error:
        print({"status": "ERROR", 'debug':error})
