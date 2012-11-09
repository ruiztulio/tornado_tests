import sqlite3
import urllib
import urllib2
import json
url = "http://192.168.173.146:8888/products/"
conn = sqlite3.connect('./sqlitelocal.db')

# Get a cursor
cursor = conn.cursor()

# Create a table
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("""CREATE TABLE products
						(
						  id integer NOT NULL,
						  name character varying NOT NULL,
						  quantity integer NOT NULL DEFAULT 0,
						  code character varying NOT NULL,
						  price real NOT NULL DEFAULT 0,
						  PRIMARY KEY (id )
						)""")

# Insert some data
req = urllib2.Request(url)
response = urllib2.urlopen(req)
the_page = response.read()
info = json.loads(the_page)
lista = []
for product in info.get('products'):
    cursor.execute("INSERT INTO products VALUES (%s, '%s', %s, '%s', %s)"
                    %(product.get('id'), product.get('name'), product.get('quantity'),
                    product.get('code'), product.get('price')))
conn.commit()

# Read the data back out
cursor.execute("SELECT * from products")
for row in cursor:
     print row

conn.close()
