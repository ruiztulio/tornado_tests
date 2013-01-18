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
#print "Sync this 100"
#res = dm.query_sync('products', limit = 10000)
#res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
#print res
# print "Sync this 100 - 100"
# res = dm.query_sync('products', limit = 100, offset=100)
# res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
# print res
# print "Sync this 100 - 200"
# res = dm.query_sync('products', limit = 100, offset=200)
# res = read_url('%s/%s'%(url, 'database'), data = {'action':'sync_this', 'table' : 'products', 'data': json.dumps(res)})
# print res

print "Full sync"
res = dm.query_sync('products')
res_sync = read_url('%s/%s'%(url, 'database'), data = {'action':'sync', 'table' : 'products', 'data': json.dumps(res)})
print "Sincronizar inserts"
if res_sync.get('response').get('inserts'):
    res = read_url('%s/%s?%s'%(url, 'database', 
								urllib.urlencode({'action' : 'query', 
													'table' : 'products', 
													'ids' : json.dumps(res_sync.get('response').get('inserts'))})))
    dm.insert_many(res.get('rows'), 'products')
    print len(res.get('rows'))
	
print "Sincronizar updates"
if res_sync.get('response').get('updates'):
    res = read_url('%s/%s?%s'%(url, 'database', 
                                urllib.urlencode({'action' : 'query', 
                                                    'table' : 'products', 
                                                    'ids' : json.dumps(res_sync.get('response').get('updates'))})))
    print len(res.get('rows'))
    dm.update_many(res.get('rows'), 'products')
print "Sincronizar uploads"
print len(res_sync.get('response').get('uploads'))
if res_sync.get('response').get('uploads'):
    data = dm.query('products', res_sync.get('response').get('uploads'))
    res = read_url('%s/%s'%(url, 'database'), 
                                data = {'action' : 'upload', 
                                                    'table' : 'products', 
                                                    'data' : json.dumps(data)})

