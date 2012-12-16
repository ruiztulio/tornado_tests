import ConfigParser
import sqlite3

class ConfigManager():
    config_file = None
    conn = None
    cursor = None

    def __init__(self):
        self.config_file = ConfigParser.ConfigParser()
        self.config_file.read('config.ini')
        self.conn = sqlite3.connect(self.config_file.get('application', 'dbname'))
        self.cursor = self.conn.cursor()

    def set(self, config):
        self.cursor.execute("""INSERT INTO config (host, user, password, port, database) 
                                VALUES (?, ?, ?, ?, ?)""", (config.get('host'), config.get('user'), config.get('password'), config.get('port'), config.get('database')))
        self.conn.commit()

    def get_database_config(self):
        self.cursor.execute("SELECT * FROM config ORDER BY id DESC LIMIT 1")
        r = self.cursor.fetchone()
        if not r:
            res = {'host' : self.config_file.get('database', 'host'),
                    'user' : self.config_file.get('database', 'user'),
                    'password':self.config_file.get('database', 'password'),
                    'port':int(self.config_file.get('database', 'port')),
                    'database':self.config_file.get('database', 'database')}
        else:
            res = {'host' : str(r[1]),
                    'user' : str(r[2]),
                    'password':str(r[3]),
                    'port':r[4],
                    'database':str(r[5])}
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
        for method in ['GET', 'POST']:
            for column in columns:
                if column != 'id':
                    self.cursor.execute("INSERT INTO methods (model_id, method_name, field_name) VALUES (?, ?, ?)", (table_id, method, column))
                else:
                    self.cursor.execute("INSERT INTO methods (model_id, method_name, field_name, use) VALUES (?, ?, ?, 1)", (table_id, method, column))
        self.conn.commit()

    def save_tables(self, tables):
        self.cursor.execute("UPDATE models SET use = 0")
        for table in tables:
            #cursor.execute("INSERT INTO models (name) VALUES (?)", (table,))
            print table
            self.cursor.execute("UPDATE models SET use = 1 WHERE id = (?)", (table,))
        self.conn.commit()
