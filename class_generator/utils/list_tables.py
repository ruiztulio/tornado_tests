#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
pg_user = "testrest"
pg_pass = "123"
pg_host ="localhost"
pg_dbname ="rest_sales"
pg_port =5432


con = None

def list_tables(database):
    res = []
    try:
        con = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                        (pg_host, database, pg_pass, pg_user, pg_port)) 
        cur = con.cursor() 
        cur.execute("""SELECT table_name FROM information_schema.tables 
                        WHERE table_schema = 'public'""")    
        rows = cur.fetchall()
        for r in rows:
            res.append(r[0])
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
    return res

def list_columns(table, database):
    res = []
    try:
        con = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                        (pg_host, database, pg_pass, pg_user, pg_port)) 
        cur = con.cursor() 
        cur.execute("""SELECT column_name FROM information_schema.columns WHERE table_name =%s""", (table,))    
        rows = cur.fetchall()
        for r in rows:
            res.append(r[0])
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
    return res

try:
     
    con = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                    (pg_host, pg_dbname, pg_pass, pg_user, pg_port)) 
    
    cur = con.cursor() 
    # cur.execute("""SELECT table_name FROM information_schema.tables 
       # WHERE table_schema = 'public'""")    
    cur.execute("""SELECT column_name FROM information_schema.columns WHERE table_name ='products'""")
    rows = list_tables('rest_sales')
    con.close()
    print rows
    for r in rows:
        c = list_columns(r, 'rest_sales')
        print c
    
   
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
