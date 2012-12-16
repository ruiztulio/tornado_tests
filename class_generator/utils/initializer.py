import sqlite3
from config_manager import ConfigManager
from tornado.options import options
from database_manager import DatabaseManager



def insert_db_tables():
    dm = DatabaseManager()
    cm = ConfigManager()
    tables = dm.list_tables()
    cm.save_tables(tables)
    for table in tables:
        model_id = cm.find_table(table)
        fields = dm.list_columns(table)
        cm.save_columns(model_id, fields)
    cm.get_models_config()

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
                            use boolean DEFAULT 0,
                            PRIMARY KEY (id)
                            )""")

    cursor.execute("""CREATE TABLE methods
                            (
                            id integer NOT NULL,
                            model_id integer NOT NULL,
                            method_name character varying NOT NULL,
                            field_name character varying NOT NULL,
                            use boolean DEFAULT 0,
                            PRIMARY KEY (id),
                            UNIQUE(method_name, field_name, model_id)
                            FOREIGN KEY(model_id) REFERENCES models(id)
                            )""")
    conn.commit()
    insert_db_tables()