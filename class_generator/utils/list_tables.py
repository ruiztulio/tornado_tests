#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
from utils import copyListDicts
from tornado.options import options



con = None
def list_databases():
    sql = '''SELECT d.datname as "name",
                u.usename as "owner",
                pg_catalog.pg_encoding_to_char(d.encoding) as "encoding"
                FROM pg_catalog.pg_database d
                LEFT JOIN pg_catalog.pg_user u ON d.datdba = u.usesysid
                ORDER BY 1;'''
    conn = psycopg2.connect("host=%s password=%s, dbname=postgres user=%s port=%s"%
                    (options.pg_host, options.pg_pass, options.pg_user, options.pg_port)) 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql)
    res = copyListDicts(cur)
    return res

def list_tables(database):
    res = []
    try:
        con = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                        (options.pg_host, database, options.pg_pass, options.pg_user, options.pg_port)) 
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
                        (options.pg_host, database, options.pg_pass, options.pg_user, options.pg_port)) 
        cur = con.cursor() 
        cur.execute("""SELECT column_name FROM information_schema.columns WHERE table_name =%s""", (table,))    
        rows = cur.fetchall()
        for r in rows:
            res.append(r[0])
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
    return res

def dummy():
    try:
         
        con = psycopg2.connect("host=%s dbname=%s password=%s user=%s port=%s"%
                        (options.pg_host, options.pg_dbname, options.pg_pass, options.pg_user, options.pg_port)) 
        
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
