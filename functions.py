import json
import psycopg2

def insert_node(obj, connection):
    query = "INSERT INTO node(id,description,coordinates) VALUES ({0},'{1}',POINT({2},{3}))".format(obj['node'],obj['description'],obj['lat'],obj['lon'])
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print({'status': 'OK'})
        return True
    except:
        cursor.close()
        print({'status': 'ERROR'})
        return False




def insert_catalog(obj,connection):
    nodesArray = obj['nodes']
    lenght = len(nodesArray)-1
    try:
        cursor = connection.cursor()
        query = "INSERT INTO catalog(version,takes_days) VALUES ({0},{1})".format(obj['version'], lenght)
        cursor.execute(query)

        for x in range(0, lenght):
            query = "INSERT INTO connection(node_order,entry_node_id,exit_node_id, version_id) VALUES ({0},{1},{2},{3})".format(x,nodesArray[x],nodesArray[x+1],obj['version'])
            cursor.execute(query)
        
        connection.commit()
        cursor.close()

        print({'status': 'OK'})
        return True
    except ValueError:
        cursor.close()
        print({'status': 'ERROR'})
        return False
