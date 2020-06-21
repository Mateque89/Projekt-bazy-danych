
import psycopg2
from functions import *

class EventHandler:
    connection = None
    isConnected = False
    def Event(self,obj):
        if 'open' in obj:
            try:
                self.connection = psycopg2.connect(dbname='student', user='app', password='qwerty', host='localhost', port='5432')
                self.isConnected = True
                return None 
            except:
                print('I am unable to connect to the database')
        if self.isConnected == True:
            body = obj['body']
            if obj['function'] =='closest_nodes':
                return None 
            if obj['function'] == 'node':
                insert_node(body,self.connection)
            if obj['function'] == 'catalog':
                insert_catalog(body,self.connection)
            if obj['function'] == 'trip':
                return None 
            if obj['function'] == 'cyclist':
                return None 
            if obj['function'] == 'party':
                return None 
            if obj['function'] == 'guests':
                return None
        else:
            print({'status': 'CONNECTION ERROR'})