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

    def get_tables_list(self):
        self.cursor.execute("""SELECT id, name, class_name, use
                                FROM models
                                ORDER BY models.name ASC""")
        rows = self.cursor.fetchall()
        return rows

    def get_models_config(self):
        self.cursor.execute("""SELECT * 
                                FROM models 
                                JOIN methods 
                                ON models.id = methods.model_id 
                                ORDER BY models.name ASC, methods.method_name, methods.field_name""")
        rows = self.cursor.fetchall()
        res = {}
        for row in rows:
            res.update({row[1] : []})
            res.get(row[1]).append
            print row
