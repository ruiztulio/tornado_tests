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
if tables.get('status').get('id') == u'OK':
    for t in tables.get('tables'):
        print t
        content = read_url('%s/%s?%s'%(url, 'database', urllib.urlencode({'action' : 'query_sync', 'table' : t[0]})))
        print content
