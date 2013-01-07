#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import logging
from utils import copyListDicts
from tornado.options import options

gen_log = logging.getLogger("tornado.general")

class DatabaseManagerBase():
    def generate_conn(self, config = None):
        raise NotImplemented()

    def list_tables(self):        
        raise NotImplemented()

    def list_columns(self, table, database = None):
        raise NotImplemented()

    def query(self, table, limit=None, offset=None):
        raise NotImplemented()

    def query_sync(self, table, limit=None, offset=None):
        raise NotImplemented()

    def insert(self, data, table):
        raise NotImplemented()

    def update(self, data, table):
        raise NotImplemented()

class DatabaseManagerPostgres(DatabaseManagerBase):
    def generate_conn(self, config = None):
        if config:
            conn_str = "host=%s password=%s dbname=%s user=%s port=%s"% \
                            (config.get('host', options.pg_host), 
                            config.get('password', options.pg_pass), 
                            config.get('database', options.pg_dbname), 
                            config.get('user', options.pg_user), 
                            config.get('port', options.pg_port))
        else:
            conn_str = "host=%s password=%s dbname=%s user=%s port=%s"% \
                            (options.pg_host, options.pg_pass, options.pg_dbname, options.pg_user, options.pg_port)
        print conn_str
        return psycopg2.connect(conn_str)

    def list_tables(self):
        res = []
        try:
            conn = self.generate_conn()
            cur = conn.cursor() 
            cur.execute("""SELECT table_name, sync_type FROM sync_tables""")    
            rows = cur.fetchall()
            print rows
            for r in rows:
                res.append( (r[0], r[1]) )
            conn.close()
        except psycopg2.DatabaseError, e:
            gen_log.error("Error listando tablas", exc_info=True)
            print 'Error %s' % e    
        return res

    def search_table(self, table):
        res = []
        try:
            conn = self.generate_conn()
            cur = conn.cursor() 
            cur.execute("""SELECT table_name, sync_type FROM sync_tables WHERE table_name=%s""",(table,))    
            rows = cur.fetchall()
            for r in rows:
                res.append( (r[0], r[1]) )
            conn.close()
        except psycopg2.DatabaseError, e:
            gen_log.error("Error listando tablas", exc_info=True)
            print 'Error %s' % e    
        return res

    def query(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        sql = """SELECT * FROM %s """%(table)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def query_sync(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        sql = """SELECT id, write_date FROM %s """%(table)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())