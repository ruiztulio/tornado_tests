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

    def get_updated(self, data):
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

    def query(self, table, ids = None, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        sql = "SELECT * FROM %s "%(table)
        if ids:
            sql = sql + "WHERE id IN ("+", ".join(["%s"]*len(ids))+")"
            print cur.mogrify(sql, ids)
            cur.execute(sql, ids)
        else:
            cur.execute(sql)
        res = copyListDicts(cur.fetchall())
        print res
        return res

    def query_sync(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        sql = """SELECT id, write_date FROM %s """%(table)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def get_updated(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        if data:
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date > %s )"]*len(data))
            for d in data:
                values = values + d.values()
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cur.execute(sql, values)
        return [r.get('id') for r in cur.fetchall()]

    def get_uploads(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        if data:
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date < %s )"]*len(data))
            for d in data:
                values = values + d.values()
        #print cur.mogrify(sql, values)
        cur.execute(sql, values)
        return [r.get('id') for r in cur.fetchall()]

    def get_full_uploads(self, data, table):
        sql = "SELECT id FROM %s "%table
        values = []
        res = []
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        if data:
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date < %s )"]*len(data))
            sql_insert = "SELECT id FROM %s WHERE id = %s"%(table, "%s")
            for d in data:
                values = values + d.values()
                cur.execute(sql_insert, (d.get('id'), ))
                if cur.rowcount == 0:
                    res.append(d.get('id'))
        #print cur.mogrify(sql, values)
        cur.execute(sql, values)
        return res+[r.get('id') for r in cur.fetchall()]

    def get_inserts(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        if data:
            #sql = sql + " NOT IN (" +  ", ".join(["%s"]*len(data)) + ")"
            sql = sql + " NOT IN (%s)"
            for d in data:
                values.append(d.get('id'))
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cur.execute(sql, values)
        return [r.get('id') for r in cur.fetchall()]

    def get_deleted(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        if data:
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            sql = sql + "WHERE id = %s "
            for d in data:
                cur.execute(sql, d.get('id'))
                print cur.rowcount
        else:
            return {}
        return [r.get('id') for r in cur.fetchall()]
