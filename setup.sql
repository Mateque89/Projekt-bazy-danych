----------------------------------------Wyczysc aktualna baze danych ( DO TESTÓW)----------------------------------------
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
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
    id integer PRIMARY KEY,
    catalog_id integer NOT NULL,
    name_id text NOT NULL,
    start_day date NOT NULL,
    end_day date NOT NULL,
    FOREIGN KEY (name_id) REFERENCES cyclist (name),
    FOREIGN KEY (catalog_id) REFERENCES catalog (version)
);

--tabela node
CREATE TABLE node(
    id integer PRIMARY KEY,
    description text NOT NULL,
    coordinates point NOT NULL
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







