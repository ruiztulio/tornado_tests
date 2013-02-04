#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import logging
from utils import copyListDicts
from tornado.options import options
from database import DatabaseManagerBase

gen_log = logging.getLogger("tornado.general")


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
            gen_log.error("Error buscando tablas", exc_info=True)
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
        res = []
        if data:
            sql = "SELECT id from %s "%table
            values = []
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date > %s )"]*len(data))
            for d in data:
                values = values + d.values()
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            cur.execute(sql, values)
            res = [r.get('id') for r in cur.fetchall()]
        return res

    def get_uploads(self, data, table):
        res = []
        if data:
            sql = "SELECT id from %s "%table
            values = []
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date < %s )"]*len(data))
            for d in data:
                values = values + d.values()
            cur.execute(sql, values)
            res = [r.get('id') for r in cur.fetchall()]
        return res

    def get_full_uploads(self, data, table):
        res = []
        if data:
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            res = self.get_uploads(data, table)
            sql_insert = "SELECT id FROM %s WHERE id = %s"%(table, "%s")
            for d in data:
                cur.execute(sql_insert, (d.get('id'), ))
                if cur.rowcount == 0:
                    res.append(d.get('id'))
        return res

    def get_inserts(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        if data:
            print "Hay dataaaaaa...", data
            sql = sql + " WHERE id NOT IN (" +  ", ".join(["%s"]*len(data)) + ")"
            #sql = sql + " WHERE id NOT IN (%s)"
            for d in data:
                values.append(d.get('id'))
            cur.execute(sql, values)
        else:
            cur.execute(sql)
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

    def save(self, data, table):
        conn = self.generate_conn()
        cur = conn.cursor() 

        for d in data:
            del d['server_act']
            f = str(tuple(str(x) for x in d)).replace("'", "")
            v = str(tuple(['%s']*len(d))).replace("'", "")
            sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s'%{'name':table, 'fields': f, 'values':v}
            try:
                cur.execute(sql, d.values())
                conn.commit()
            except psycopg2.IntegrityError, e:
                fields = ", ".join(['%s = %s'%(f, "%s") for f in d])
                sql = "UPDATE %(name)s SET %(fields)s WHERE id = '%(id)s'"%{'name':table, 'fields': fields, 'id': d.get('id')}
                conn.rollback()
                cur.execute(sql, d.values())
                conn.commit()
