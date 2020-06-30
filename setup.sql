--CREATE EXTENSION postgis;
----------------------------------------Wyczysc aktualna baze danych ( DO TESTÓW)----------------------------------------
DROP TABLE  cyclist cascade;
DROP TABLE  catalog cascade;
DROP TABLE  reservation cascade;
DROP TABLE  node cascade;
DROP TABLE  connection cascade;
------------------------------------------------------------------------------------------------------------------------


--Inicjalizacja bazy danych
--Szymon Pielat 
--308859

----------------------------------------tabele----------------------------------------

--tabela rowerzysta
CREATE TABLE cyclist(
    name text PRIMARY KEY,
    distance_traveled float DEFAULT 0,
    no_trips integer DEFAULT 0
);

--tabela tras rowerowych
CREATE TABLE catalog(
    version integer PRIMARY KEY,
    takes_days integer NOT NULL
);

--tabela rezerwacji
CREATE TABLE reservation(
    id SERIAL PRIMARY KEY,
    catalog_id integer NOT NULL,
    name_id text NOT NULL,
    start_day date NOT NULL,
    FOREIGN KEY (name_id) REFERENCES cyclist (name),
    FOREIGN KEY (catalog_id) REFERENCES catalog (version)
);

--tabela node
CREATE TABLE node(
    id integer PRIMARY KEY,
    description text NOT NULL,
    coordinates GEOGRAPHY(Point) NOT NULL
);

--tabela polączenia miedzy punktami
CREATE TABLE connection(
    id SERIAL PRIMARY KEY,
    node_order integer NOT NULL,
    exit_node_id integer NOT NULL,
    entry_node_id integer NOT NULL,
    version_id integer,
    FOREIGN KEY (entry_node_id) REFERENCES node (id),
    FOREIGN KEY (exit_node_id) REFERENCES node (id),
    FOREIGN KEY (version_id) REFERENCES catalog (version)
);


create INDEX on node using Gist (coordinates);

----------------------------------------funkcje----------------------------------------
---Liczenie dla danej trasy jej dlugosci
CREATE OR REPLACE FUNCTION calculate_distance(integer) RETURNS integer AS $$
DECLARE
    distance integer := 0;
    x record;
BEGIN
    FOR x IN 
    SELECT * FROM connection WHERE version_id=$1
    LOOP
        distance = distance + ST_Distance((SELECT coordinates FROM node WHERE x.exit_node_id = id), (SELECT coordinates FROM node WHERE x.entry_node_id = id));
    END LOOP;
  RETURN ROUND(distance);
END
$$ LANGUAGE plpgsql; 

---Aktualizacja rowerzysty oraz dodawanie rezerwacji;
CREATE OR REPLACE FUNCTION add_reservation(Fname text,Fcatalog integer, Fstart_day date) RETURNS VOID AS $$
BEGIN ---sprawdz czy rowerzysta istnieje
    IF Fname NOT IN (SELECT name FROM cyclist) THEN 
        -- nie ma go w bazie czyli go dodaj
        INSERT INTO cyclist(name,distance_traveled,no_trips) VALUES (Fname,calculate_distance(Fcatalog), 1);
    ELSE
        -- jest juz, wiec tylko powieksz mu wynik
        UPDATE cyclist SET distance_traveled = distance_traveled + calculate_distance(Fcatalog), no_trips=no_trips+1 WHERE name=Fname;
    END IF;
    --Dodaj rezerwacje
    INSERT INTO reservation(catalog_id,name_id,start_day) VALUES (Fcatalog, Fname, Fstart_day);
END
$$ LANGUAGE plpgsql; 

--- Znajdz gosci ktorzy beda spac w danym miejscu danego dnia
CREATE OR REPLACE FUNCTION find_guest(Fnode integer, Fdate date) RETURNS TABLE (guest text) AS $$
BEGIN  
    RETURN QUERY (SELECT DISTINCT reservation.name_id FROM reservation, connection WHERE (connection.node_order)=(Fdate-reservation.start_day) AND exit_node_id=Fnode );
END
$$ LANGUAGE plpgsql; 

