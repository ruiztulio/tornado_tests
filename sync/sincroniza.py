import sqlite3
import urllib
import urllib2
import json
import psycopg2
import psycopg2.extras

url = "http://localhost:8881/products"
conn = sqlite3.connect('./sqlitelocal.db')
cursor = conn.cursor()

pg_user="testrest"
pg_pass="123"
pg_host="localhost"
pg_dbname="rest_sales"
pg_port=5432

#~ conn = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                            #~ (pg_host, pg_dbname, pg_pass, pg_user, pg_port))
#~ conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#~ cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
def get_products():
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
        campos = product.keys()
        sql = "INSERT INTO products ("
        v = " ("
        for c in campos:
            sql += c + ", "
            v += "?, "
        sql = sql[:-2] + ") VALUES " + v[:-2] + ")"
        print sql
        print campos
        v = (product.get(k) for k in campos)
        cursor.execute(sql, v)
    conn.commit()

def get_clients():
    cursor = conn.cursor()
    # Create a table
    cursor.execute("DROP TABLE IF EXISTS clients")
    cursor.execute("""CREATE TABLE clients
                    (
                    id integer NOT NULL,
                    name character varying NOT NULL,
                    address character varying NOT NULL,
                    phone character varying,
                    vat character varying NOT NULL,
                    PRIMARY KEY (id )
                    )""")
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
#cursor = conn.cursor()
#~ cursor.execute("\\d+ products")
#~ for row in cursor:
    #~ print row
get_products()
conn.close()
