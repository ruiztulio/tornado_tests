#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import uuid
from lib.utils import copyListDicts
from databasemanager_base import DatabaseManagerClientBase

class DatabaseManagerClientSqlite(DatabaseManagerClientBase):
    def generate_conn(self, config = None):
		return sqlite3.connect('client.db', row_factory=sqlite3.Row)

    def query(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor() 
        sql = """SELECT * FROM %s """%(table)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def query_sync(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor() 
        sql = """SELECT id, write_date FROM %s """%(table)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def insert(self, data, table, gen_write_date = False):
		data.update({'id': str(uuid.uuid4())})
		f = str(tuple(data)).replace("'", "")
		v = str(tuple(['%s']*len(data))).replace("'", "")
		sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s'%{'name':table, 'fields': f, 'values':v}
		conn = self.generate_conn()
		cur = conn.cursor() 
		cur.execute(sql)
		cur.commit()

        

    def update(self, data, table):
        raise NotImplemented()

