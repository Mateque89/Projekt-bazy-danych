import json
import psycopg2

def insert_node(obj, connection):
    query = "INSERT INTO node(id,description,coordinates) VALUES ({0},'{1}','SRID=4326;POINT({2} {3})')".format(obj['node'],obj['description'],obj['lat'],obj['lon'])
    cursor = connection.cursor()
    try:
        print(query)
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
    except:
        cursor.close()
        print({'status': 'ERROR'})
        return False


def insert_biker(obj,connection):
    query = "INSERT INTO reservation(catalog_id,name_id,start_day) VALUES ({0},'{1}','{2}')".format(obj['version'],obj['cyclist'],obj['date'])
    print(query)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print({'status': 'OK'})
    except:
        cursor.close()
        print({'status': 'ERROR'})
        return False
