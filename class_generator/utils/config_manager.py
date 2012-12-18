import ConfigParser
import sqlite3
import os

class ConfigManager():
    config_file = None
    conn = None
    cursor = None

    def __init__(self):
        if not os.path.isfile('config.ini'):
            raise IOError("No se encuentra el archivo config.ini")

        self.config_file = ConfigParser.ConfigParser()
        self.config_file.read('config.ini')
        self.conn = sqlite3.connect(self.config_file.get('application', 'dbname'))
        self.cursor = self.conn.cursor()

    def set(self, config):
        self.cursor.execute("""INSERT INTO config (host, user, password, port, database) 
                                VALUES (?, ?, ?, ?, ?)""", (config.get('host'), config.get('user'), config.get('password'), config.get('port'), config.get('database')))
        self.conn.commit()

    def get_database_config(self):
        res = {'host' : self.config_file.get('database', 'host'),
                'user' : self.config_file.get('database', 'user'),
                'password':self.config_file.get('database', 'password'),
                'port':int(self.config_file.get('database', 'port')),
                'database':self.config_file.get('database', 'database')}
        if os.path.isfile(self.get('application', 'dbname')):
            try:
                self.cursor.execute("SELECT * FROM config ORDER BY id DESC LIMIT 1")
                r = self.cursor.fetchone()
                if r:
                    res = {'host' : str(r[1]),
                            'user' : str(r[2]),
                            'password':str(r[3]),
                            'port':r[4],
                            'database':str(r[5])}
            except sqlite3.OperationalError:
                pass
            
        return res

    def get(self, *args):
        if len(args) < 2:
            raise TypeError("get() takes at least 2 arguments (%s given)"%(len(args)))
        section, item = args
        if section == 'database':
            return self.get_database_config()[item]
        return self.config_file.get(section, item)

    def get_tables_list(self, use = None):
        if use is not None:
            self.cursor.execute("""SELECT id, name, class_name, use
                                    FROM models
                                    WHERE use = ?
                                    ORDER BY models.name ASC""", (use,))
        else:
            self.cursor.execute("""SELECT id, name, class_name, use
                                    FROM models
                                    ORDER BY models.name ASC""")
        rows = self.cursor.fetchall()
        return rows

    def get_methods(self, model_id):
        self.cursor.execute("""SELECT distinct method_name
                                FROM methods""")
        res = []
        rows = self.cursor.fetchall()
        for r in rows:
            res.append(r[0])
        return res

    def get_methods_fields(self, method, model_id, use = None):
        if not use:
            self.cursor.execute("""SELECT field_name
                                    FROM methods
                                    WHERE method_name = ?
                                    AND model_id = ?""", (method, model_id,))
        else:
            self.cursor.execute("""SELECT field_name
                                    FROM methods
                                    WHERE method_name = ?
                                    AND use = 1
                                    AND model_id = ?""", (method, model_id,))
        res = []
        rows = self.cursor.fetchall()
        for r in rows:
            res.append(r[0])
        return res

    def get_models_config(self):
        models = self.get_tables_list(True)

        res = {}
        for model in models:
            res.update({model[1] : {}})
            self.cursor.execute("""SELECT id, field_name, method_name, use 
                                    FROM methods 
                                    WHERE model_id = ?
                                    AND method_name = 'GET'
                                    ORDER BY method_name, field_name""", (model[0],))
            rows = self.cursor.fetchall()
            res.get(model[1]).update({'GET' : []})
            for row in rows:
                res.get(model[1]).get('GET').append(row)

            self.cursor.execute("""SELECT id, field_name, method_name, use 
                                    FROM methods 
                                    WHERE model_id = ?
                                    AND method_name = 'POST'
                                    ORDER BY method_name, field_name""", (model[0],))
            rows = self.cursor.fetchall()
            res.get(model[1]).update({'POST' : []})
            for row in rows:
                res.get(model[1]).get('POST').append(row)
        return res

    def find_table(self, table):
        self.cursor.execute("""SELECT * FROM models WHERE name = ? LIMIT 1""", (table,))
        row = self.cursor.fetchone()
        return row[0]

    def save_columns(self, table_id, columns):
        for method in ['GET', 'POST', 'DELETE', 'PUT']:
            for column in columns:
                if column != 'id' or (method == 'POST' and column == 'id'):
                    self.cursor.execute("INSERT INTO methods (model_id, method_name, field_name) VALUES (?, ?, ?)", (table_id, method, column))
                else:
                    self.cursor.execute("INSERT INTO methods (model_id, method_name, field_name, use) VALUES (?, ?, ?, 1)", (table_id, method, column))
        self.conn.commit()

    def save_tables(self, tables):
        for table in tables:
            self.cursor.execute("INSERT INTO models (name, use) VALUES (?, 0)", (table,))
            print table
        self.conn.commit()

    def update_tables(self, tables):
        self.cursor.execute("UPDATE models SET use = 0")
        for table in tables:
            #cursor.execute("INSERT INTO models (name) VALUES (?)", (table,))
            print table
            self.cursor.execute("UPDATE models SET use = 1 WHERE id = (?)", (table,))
        self.conn.commit()

    def update_config_method(self, method, table_id, column_ids):
        self.cursor.execute("UPDATE methods SET use = 0 WHERE field_name <> 'id' AND method_name = ? AND model_id = ?", (method, table_id,))
        if method != 'POST':
            self.cursor.execute("UPDATE methods SET use = 1 WHERE field_name = 'id' AND method_name = ? AND model_id = ?", (method, table_id,))
        self.conn.commit()
        for column_id in column_ids:
            self.cursor.execute("UPDATE methods SET use = 1 WHERE field_name <> 'id' AND id = ?", (column_id,))
        self.conn.commit()

    def update_config_model(self, table_id, name):
        self.cursor.execute("UPDATE models SET class_name = ? WHERE id = ? ", (name, table_id,))
        self.conn.commit()
 