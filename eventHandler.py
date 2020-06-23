
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
                print({'status': 'CONNECTED'})
                return None 
            except:
                print({'status':'UNABLE TO CONNECT TO THE DATABASE'})
        if self.isConnected == True:
            body = obj['body']
            if obj['function'] =='closest_nodes':
                return None 
            if obj['function'] == 'node':
                insert_node(body,self.connection)
            if obj['function'] == 'catalog':
                insert_catalog(body,self.connection)
            if obj['function'] == 'trip':
                insert_biker(body,self.connection)
            if obj['function'] == 'cyclist':
                return None 
            if obj['function'] == 'party':
                return None 
            if obj['function'] == 'guests':
                return None
        else:
            print({'status': 'CONNECTION ERROR'})