#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import uuid
from lib.utils import copyListDicts
from databasemanager_base import DatabaseManagerClientBase
import time

class DatabaseManagerClientSqlite(DatabaseManagerClientBase):
    def generate_conn(self, config = None):
        conn = sqlite3.connect('client.db')
        conn.row_factory=sqlite3.Row
        return conn

    def query(self, table, ids=None, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor() 
        sql = "SELECT * FROM %s "%(table)
        if ids:
            sql = sql + "WHERE id IN ("+", ".join(["?"]*len(ids))+")"
            cur.execute(sql, ids)
        else:
            cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def query_sync(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor() 
        print "Limit : ", limit
        sql = """SELECT id, write_date FROM %s """%(table)
        if limit:
            sql = '%s LIMIT %s'%(sql, limit)
            if offset:
                sql = '%s OFFSET %s'%(sql, offset)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def insert(self, data, table, gen_id=False, gen_write_date=False):
        if gen_id:
            data.update({'id': str(uuid.uuid4())})
		#if gen_write_date:
		#	data.update({'write_date':  })
        f = str(tuple(str(x) for x in data)).replace("'", "")
        v = str(tuple(['?']*len(data))).replace("'", "")
        sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s'%{'name':table, 'fields': f, 'values':v}
        print data.get('id')
        conn = self.generate_conn()
        cur = conn.cursor() 
        cur.execute(sql, data.values())
        conn.commit()

    def insert_many(self, data, table, gen_id=False, gen_write_date=False):
        conn = self.generate_conn()
        cur = conn.cursor() 
        for d in data:
            if gen_id:
                d.update({'id': str(uuid.uuid4())})
        #if gen_write_date:
        #   data.update({'write_date':  })
            f = str(tuple(str(x) for x in d)).replace("'", "")
            v = str(tuple(['?']*len(d))).replace("'", "")
            sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s'%{'name':table, 'fields': f, 'values':v}
            print "%s - %s" % (table, d.get('id'))
            cur.execute(sql, d.values())
        conn.commit()

    def update(self, data, table):
        raise NotImplemented()

    def update_many(self, data, table):
        conn = self.generate_conn()
        cur = conn.cursor() 
        for d in data:
            fields = ", ".join(['%s = ?'%f for f in d])
            sql = "UPDATE %(name)s SET %(fields)s WHERE id = '%(id)s'"%{'name':table, 'fields': fields, 'id': d.get('id')}
            print "%s - %s" % (table, d.get('id'))
            cur.execute(sql, d.values())
        conn.commit()