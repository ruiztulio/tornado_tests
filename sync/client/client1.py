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
# tables = read_url('%s/%s?%s'%(url, 'database', urllib.urlencode({'action' : 'list_tables'})))
# if tables.get('status').get('id') == u'OK':
#      for t in tables.get('tables'):
#         rows = read_url('%s/%s?%s'%(url, 'database', urllib.urlencode({'action' : 'query', 'table' : t[0]})))
#         dm.insert_many(rows.get('rows'), t[0])
#         for r in rows.get('rows'):
# 			dm.insert(r, t[0])

# Sync tests
# print "Sync this all"
# res = dm.query_sync('products')
# res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
# print res
print "Sync this 100"
res = dm.query_sync('products', limit = 10000)
res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
print res
# print "Sync this 100 - 100"
# res = dm.query_sync('products', limit = 100, offset=100)
# res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
# print res
# print "Sync this 100 - 200"
# res = dm.query_sync('products', limit = 100, offset=200)
# res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
# print res
print "Full sync"
res = dm.query_sync('products', limit = 10)
res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync', 'table' : 'products', 'data': json.dumps(res)})
print res
