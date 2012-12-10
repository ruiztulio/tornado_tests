import ConfigParser
import sqlite3
import os.path
from config_manager import ConfigManager

def create_tables():
    config = ConfigManager()
    conn = sqlite3.connect(config.get('application', 'dbname'))
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS config")
    cursor.execute("DROP TABLE IF EXISTS methods")
    cursor.execute("DROP TABLE IF EXISTS models")

    cursor.execute("""CREATE TABLE config
                            (
                            id integer NOT NULL,
                            host character varying NOT NULL,
                            user character varying NOT NULL,
                            password character varying NOT NULL,
                            port integer NOT NULL,
                            database character varying NOT NULL,
                            PRIMARY KEY (id)
                            )""")

    cursor.execute("""CREATE TABLE models
                            (
                            id integer NOT NULL,
                            name character varying NOT NULL,
                            class_name character varying,
                            PRIMARY KEY (id)
                            )""")

    cursor.execute("""CREATE TABLE methods
                            (
                            id integer NOT NULL,
                            model_id integer NOT NULL,
                            method_name character varying NOT NULL,
                            field_name character varying NOT NULL,
                            PRIMARY KEY (id),
                            UNIQUE(method_name, field_name)
                            FOREIGN KEY(model_id) REFERENCES models(id)
                            )""")
    conn.commit()
