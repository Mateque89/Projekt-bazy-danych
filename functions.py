import json
import psycopg2




def buildDataBase(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(open('setup.sql').read())
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.rollback()
    

def insert_node(obj, connection):
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO node(id,description,coordinates) VALUES (%s,%s,'SRID=4326;POINT(%s %s)')",
                       (obj['node'], obj['description'], obj['lon'], obj['lat']))
        connection.commit()
        cursor.close()
        print({'status': 'OK'})
        return True
    except (Exception) as error:
        cursor.close()
        print({"status": "ERROR", 'debug':error})
        return False


def insert_catalog(obj, connection):
    nodesArray = obj['nodes']
    lenght = len(nodesArray)-1
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO catalog(version,takes_days) VALUES (%s,%s)", (obj['version'], lenght))

        for x in range(0, lenght):
            cursor.execute("INSERT INTO connection(node_order,entry_node_id,exit_node_id, version_id) VALUES (%s,%s,%s,%s)",
                           (x, nodesArray[x], nodesArray[x+1], obj['version']))

        connection.commit()
        cursor.close()

        print({'status': 'OK'})
        return True
    except (Exception) as error:
        cursor.close()
        print({"status": "ERROR", 'debug':error})
        return False


def insert_biker(obj, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT add_reservation(%s,%s,%s)",
                       (obj['cyclist'], obj['version'], obj['date']))
        connection.commit()
        cursor.close()
        print({'status': 'OK'})
        return True
    except (Exception) as error:
        cursor.close()
        print({"status": "ERROR", 'debug':error})
        return False


def get_closest_nodes(obj, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT node.id, ST_X(node.coordinates::geometry), ST_Y(node.coordinates::geometry),distance FROM node,ROUND(ST_Distance(node.coordinates, 'SRID=4326;POINT(%s %s)')) AS distance WHERE distance <20000 ORDER BY distance ASC LIMIT 3", (obj['ilon'], obj['ilat']))
        result = cursor.fetchall()
        array = []

        for row in result:
            array.append(
                {'node': row[0], 'olat': row[2], 'olon': row[1], 'distance': int(row[3])})
        cursor.close()
        result = {'status': 'OK', 'data': array}
        print(result)
        return result
    except (Exception) as error:
        cursor.close()
        print({"status": "ERROR", 'debug':error})
        return False


def get_guest(obj, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT find_guest(%s,%s)", (obj['node'], obj['date']))
        result = cursor.fetchall()
        array = []

        for row in result:
            array.append({'cyclist': row[0]})
        cursor.close()

        result = {'status': 'OK', 'data': array}
        print(result)
        return result
    except (Exception) as error:
        cursor.close()
        print({"status": "ERROR", 'debug':error})
        return False


def get_cyclist(obj, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM cyclist ORDER BY distance_traveled ASC, name ASC LIMIT %s", [obj['limit']])
        result = cursor.fetchall()
        array = []
        for row in result:
            array.append(
                {'cyclist': row[0], 'distance': int(row[1]), 'no_trips': row[2]})
        cursor.close()
        result = {'status': 'OK', 'data': array}
        print(result)
        return result
    except (Exception) as error:
        cursor.close()
        print({"status": "ERROR", 'debug':error})
        return False
