
import psycopg2
from functions import *
import sys

class EventHandler:
    connection = None
    isConnected = False
    
    def Event(self, obj):
        if 'open' in obj:
            try:
                body = obj['open']
                self.connection = psycopg2.connect(
                    dbname=body['database'], user=body['login'], password=body['password'])
                self.isConnected = True
                if len(sys.argv) == 2:
                    if(sys.argv[1]=='--init'):
                        buildDataBase(self.connection)
                print({'status': 'CONNECTED'})
                return None
            except:
                print({'status': 'UNABLE TO CONNECT TO THE DATABASE'})
        if self.isConnected == True:
            body = obj['body']
            if obj['function'] == 'closest_nodes':
                get_closest_nodes(body, self.connection)
            if obj['function'] == 'node':
                insert_node(body, self.connection)
            if obj['function'] == 'catalog':
                insert_catalog(body, self.connection)
            if obj['function'] == 'trip':
                insert_biker(body, self.connection)
            if obj['function'] == 'cyclists':
                get_cyclist(body, self.connection)
            if obj['function'] == 'guests':
                get_guest(body, self.connection)
        else:
            print({'status': 'CONNECTION ERROR'})


