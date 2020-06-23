CREATE EXTENSION postgis;
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
    --end_day date NOT NULL,
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


----------------------------------------funkcje----------------------------------------

---Liczenie dla danej trasy jej dlugosci
CREATE OR REPLACE FUNCTION calculate_distance(integer) RETURNS integer AS $$
DECLARE
    distance float := 0;
    x record;
BEGIN
    FOR x IN 
    SELECT * FROM connection WHERE version_id=$1
    LOOP
        distance = distance + ST_Distance((SELECT coordinates FROM node WHERE x.exit_node_id = id), (SELECT coordinates FROM node WHERE x.entry_node_id = id));
    END LOOP;
  RETURN distance;
END
$$ LANGUAGE plpgsql; 

---Dopisywanie kilometrow i dni rowerzyscie(jezeli jest to nowy rowerzysta dodaje go do bazy)
CREATE OR REPLACE FUNCTION update_cyclist() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.name_id NOT IN (SELECT name FROM cyclist) THEN
        INSERT INTO cyclist(name,distance_traveled,no_trips) VALUES (OLD.name_id,calculate_distance(OLD.catalog_id), 1);
    END IF;
    RETURN NEW;
END
$$ LANGUAGE plpgsql; 


---------------------------------------trigery----------------------------------------
CREATE TRIGGER cyclist_progress 
BEFORE INSERT
    ON reservation
    FOR EACH STATEMENT
       EXECUTE PROCEDURE update_cyclist();
