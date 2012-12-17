#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
from utils import copyListDicts
from tornado.options import options
from config_manager import ConfigManager


con = None
class DatabaseManager():
    def generate_conn(self, config = None):
        if config:
            conn_str = "host=%s password=%s dbname=%s user=%s port=%s"% \
                            (config.get('host', options.pg_host), 
                            config.get('password', options.pg_pass), 
                            config.get('database', options.pg_dbname), 
                            config.get('user', options.pg_user), 
                            config.get('port', options.pg_port))
        else:
            conn_str = "host=%s password=%s dbname=postgres user=%s port=%s"% \
                            (options.pg_host, options.pg_pass, options.pg_user, options.pg_port)
        return psycopg2.connect(conn_str)

    def list_databases(self):
        sql = '''SELECT d.datname as "name",
                    u.usename as "owner",
                    pg_catalog.pg_encoding_to_char(d.encoding) as "encoding"
                    FROM pg_catalog.pg_database d
                    LEFT JOIN pg_catalog.pg_user u ON d.datdba = u.usesysid
                    ORDER BY 1;'''
        conn = self.generate_conn({'database':'postgres'})
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        res = copyListDicts(cur)
        conn.close()
        return res

    def list_tables(self, database = None):
        res = []
        try:
            conn = self.generate_conn({'database':database and database or options.pg_dbname})
            cur = conn.cursor() 
            cur.execute("""SELECT table_name FROM information_schema.tables 
                            WHERE table_schema = 'public'""")    
            rows = cur.fetchall()
            for r in rows:
                print "Tabla ", r
                res.append(r[0])
            conn.close()
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e    
        return res

    def list_columns(self, table, database = None):
        res = []
        try:
            conn = self.generate_conn({'database':database and database or options.pg_dbname})
            cur = conn.cursor() 
            cur.execute("""SELECT column_name FROM information_schema.columns WHERE table_name =%s""", (table,))    
            rows = cur.fetchall()
            for r in rows:
                res.append(r[0])
            conn.close()
        except psycopg2.DatabaseError, e:
            print 'Error %s' % e    
        return res
