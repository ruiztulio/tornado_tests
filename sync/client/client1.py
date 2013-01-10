#!/usr/bin/python
# -*- coding: utf-8 -*-

from lib.databasemanager_sqlite import DatabaseManagerClientSqlite
import urllib
import urllib2
import json

url = "http://localhost:8888"

def read_url(url, data = None):
    if data:
        #res = json.dumps(data)
        res = urllib.urlencode(data, True)
        req = urllib2.Request(url, res)
    else:
        req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return json.loads(the_page)

dm = DatabaseManagerClientSqlite()
# tables = read_url('%s/%s?%s'%(url, 'database', {'action' : 'list_tables'}))
# if tables.get('status').get('id') == u'OK':
#     for t in tables.get('tables'):
#         rows = read_url('%s/%s?%s'%(url, 'database', {'action' : 'query', 'table' : t[0]}))
#         dm.insert_many(rows.get('rows'), t[0])
#        for r in rows.get('rows'):
#			dm.insert(r, t[0])

# Sync tests

res = dm.query_sync('products', limit = 2)
res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'data': json.dumps(res)})