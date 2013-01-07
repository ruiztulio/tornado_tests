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
print urllib.urlencode({'action' : 'list_tables'})
tables = read_url('%s/%s?%s'%(url, 'database', urllib.urlencode({'action' : 'list_tables'})))
print tables
