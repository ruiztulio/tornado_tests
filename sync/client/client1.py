#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.databasemanager_sqlite import DatabaseManagerClientSqlite
import urllib
import urllib2
import json

url = "http://localhost:8888"

def read_url(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return json.loads(the_page)

dm = DatabaseManagerClientSqlite()
tables = read_url('%s/%s?%s'%(url, 'database', urllib.urlencode({'action' : 'list_tables'})))
res = dm.query_sync('products')
print res
if tables.get('status').get('id') == u'OK':
    for t in tables.get('tables'):
        rows = read_url('%s/%s?%s'%(url, 'database', urllib.urlencode({'action' : 'query', 'table' : t[0]})))
        dm.insert_many(rows.get('rows'), t[0])
#        for r in rows.get('rows'):
#			dm.insert(r, t[0])
