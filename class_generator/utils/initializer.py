import ConfigParser
import sqlite3


def create_tables():
    config = ConfigParser.ConfigParser()
    config.read('../config.ini')

    conn = sqlite3.connect('../%s'%config.get('application', 'dbname'))
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS config")
    cursor.execute("DROP TABLE IF EXISTS methods")
    cursor.execute("DROP TABLE IF EXISTS tables")

    cursor.execute("""CREATE TABLE config
                            (
                            id integer NOT NULL,
                            host character varying NOT NULL,
                            user character varying NOT NULL,
                            password character varying NOT NULL,
                            port integer NOT NULL,
                            PRIMARY KEY (id)
                            )""")

    cursor.execute("""CREATE TABLE tables
                            (
                            id integer NOT NULL,
                            name character varying NOT NULL,
                            PRIMARY KEY (id)
                            )""")

    cursor.execute("""CREATE TABLE methods
                            (
                            id integer NOT NULL,
                            table_id integer NOT NULL,
                            method_name character varying NOT NULL,
                            field_name character varying NOT NULL,
                            PRIMARY KEY (id),
                            UNIQUE(method_name, field_name)
                            FOREIGN KEY(table_id) REFERENCES tables(id),
                            )""")
    conn.commit()
