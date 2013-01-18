#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import logging
from utils import copyListDicts
from tornado.options import options

gen_log = logging.getLogger("tornado.general")

class DatabaseManagerBase():
    """
    Las implementaciones de las clases para manejar la sincronizacion del lado del servidor deben heredar
    de esta clase e implementar los metodos segun se indica en la documentacion de cada uno de modo tal que 
    no sea necesario realizar ninguna modificacion en los algoritmos
    """
    def generate_conn(self, config = None):
        """
        Genera una conexion para realizar las consultas
        Kwargs:
            config (str): configuracion de la conexion a usar, se adapta segun la implementacion

        Returns:
            Una conexion del tipo de la base de datos
        """
        raise NotImplemented()

    def list_tables(self):
        """
        Lista las tablas y las configuraciones, es decir, el tipo de sincronizacion que permiten

        Returns:
            Una lista de tuplas con el nombre de la tabla y el tipo de sincronizacion:
            [('tabla1', 'ul'), ('tabla1', 'dl')...]
        """
        raise NotImplemented()

    def query(self, table, ids = None, limit=None, offset=None):
        """
        Consulta todos los campos de la tabla indicada retornando una lista de diccionarios

        Args:
            table (str): nombre de la tabla que se desea consultar

        Kwargs:
            ids (list, tuple): lista o tupla con los ids que se desean consultar, 
                el parametro es opcional, si no se pasa se asume que se consultan todos los registros

            limit (int): entero indicando la cantidad de registros que se desean consultar,
                se asume None por defecto lo cual implica que no hay limite en la consulta

            offset (int): entero que indica el registro a partir del cual se hara la consulta,
                por defecto es None lo que implica que sera desde el registro 0, si el parametro
                limit es None se ignora el offset

        Returns:
            Una lista de diccionarios con el resultado de la consulta:
            [{'id':111111, 'write_date': '2013-01-07T16:54:07.876325', 'campo1': valor...}, 
             {'id':222222, 'write_date': '2013-01-07T16:54:07.876325', 'campo1': valor2...},
              ........]
        """
        raise NotImplemented()

    def query_sync(self, table, limit=None, offset=None):
        """
        Retorna una lista de diccionarios que contienen el id y el timestamp del registro

        Args:
            table (str): nombre de la tabla que se desea consultar

        Kwargs:
            ids (list, tuple): lista o tupla con los ids que se desean consultar, 
                el parametro es opcional, si no se pasa se asume que se consultan todos los registros

            limit (int): entero indicando la cantidad de registros que se desean consultar,
                se asume None por defecto lo cual implica que no hay limite en la consulta

            offset (int): entero que indica el registro a partir del cual se hara la consulta,
                por defecto es None lo que implica que sera desde el registro 0, si el parametro
                limit es None se ignora el offset

        Returns:
            Una lista de diccionarios con el id y el timestamp:
            [{'id':111111, 'write_date': '2013-01-07T16:54:07.876325'}, 
             {'id':222222, 'write_date': '2013-01-07T16:54:07.876325'},
              ........]
        """
        raise NotImplemented()

    def insert(self, data, table, generate_id = False):
        """
        Inserta el registro contenido en data en la tabla indicada

        Args:
            data (dict): diccionario con el registro a insertar

            table (str): nombre de la tabla en la que se insertaran los registros

        Kwargs:
            generate_id (bool): Si se desea que la aplicacion genere el id del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

        Returns:
            El id del registro insertado
        """
        raise NotImplemented()

    def update(self, data, table):
        """
        Actualiza el registro contenido en data en la tabla indicada

        Args:
            data (dict): diccionario con el registro a insertar

            table (str): nombre de la tabla en la que se insertaran los registros

        Returns:
            El id del registro actualizado o falso en caso negativo
        """
        raise NotImplemented()

    def get_updated(self, data, table):
        raise NotImplemented()

    def get_uploads(self, data, table):
        raise NotImplemented()

    def get_full_uploads(self, data, table):
        raise NotImplemented()

class DatabaseManagerPostgres(DatabaseManagerBase):
    def generate_conn(self, config = None):
        if config:
            conn_str = "host=%s password=%s dbname=%s user=%s port=%s"% \
                            (config.get('host', options.pg_host), 
                            config.get('password', options.pg_pass), 
                            config.get('database', options.pg_dbname), 
                            config.get('user', options.pg_user), 
                            config.get('port', options.pg_port))
        else:
            conn_str = "host=%s password=%s dbname=%s user=%s port=%s"% \
                            (options.pg_host, options.pg_pass, options.pg_dbname, options.pg_user, options.pg_port)
        return psycopg2.connect(conn_str)

    def list_tables(self):
        res = []
        try:
            conn = self.generate_conn()
            cur = conn.cursor() 
            cur.execute("""SELECT table_name, sync_type FROM sync_tables""")    
            rows = cur.fetchall()
            print rows
            for r in rows:
                res.append( (r[0], r[1]) )
            conn.close()
        except psycopg2.DatabaseError, e:
            gen_log.error("Error listando tablas", exc_info=True)
            print 'Error %s' % e    
        return res

    def search_table(self, table):
        res = []
        try:
            conn = self.generate_conn()
            cur = conn.cursor() 
            cur.execute("""SELECT table_name, sync_type FROM sync_tables WHERE table_name=%s""",(table,))    
            rows = cur.fetchall()
            for r in rows:
                res.append( (r[0], r[1]) )
            conn.close()
        except psycopg2.DatabaseError, e:
            gen_log.error("Error buscando tablas", exc_info=True)
            print 'Error %s' % e    
        return res

    def query(self, table, ids = None, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        sql = "SELECT * FROM %s "%(table)
        if ids:
            sql = sql + "WHERE id IN ("+", ".join(["%s"]*len(ids))+")"
            print cur.mogrify(sql, ids)
            cur.execute(sql, ids)
        else:
            cur.execute(sql)
        res = copyListDicts(cur.fetchall())
        print res
        return res

    def query_sync(self, table, limit=None, offset=None):
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        sql = """SELECT id, write_date FROM %s """%(table)
        cur.execute(sql)
        return copyListDicts(cur.fetchall())

    def get_updated(self, data, table):
        res = []
        if data:
            sql = "SELECT id from %s "%table
            values = []
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date > %s )"]*len(data))
            for d in data:
                values = values + d.values()
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            cur.execute(sql, values)
            res = [r.get('id') for r in cur.fetchall()]
        return res

    def get_uploads(self, data, table):
        res = []
        if data:
            sql = "SELECT id from %s "%table
            values = []
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            sql = sql + "WHERE " +  " or ".join(["(id = %s AND write_date < %s )"]*len(data))
            for d in data:
                values = values + d.values()
            cur.execute(sql, values)
            res = [r.get('id') for r in cur.fetchall()]
        return res

    def get_full_uploads(self, data, table):
        res = []
        if data:
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            res = self.get_uploads(data, table)
            sql_insert = "SELECT id FROM %s WHERE id = %s"%(table, "%s")
            for d in data:
                cur.execute(sql_insert, (d.get('id'), ))
                if cur.rowcount == 0:
                    res.append(d.get('id'))
        return res

    def get_inserts(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        conn = self.generate_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        if data:
            print "Hay dataaaaaa...", data
            sql = sql + " WHERE id NOT IN (" +  ", ".join(["%s"]*len(data)) + ")"
            #sql = sql + " WHERE id NOT IN (%s)"
            for d in data:
                values.append(d.get('id'))
            cur.execute(sql, values)
        else:
            cur.execute(sql)
        return [r.get('id') for r in cur.fetchall()]

    def get_deleted(self, data, table):
        sql = "SELECT id from %s "%table
        values = []
        if data:
            conn = self.generate_conn()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
            sql = sql + "WHERE id = %s "
            for d in data:
                cur.execute(sql, d.get('id'))
                print cur.rowcount
        else:
            return {}
        return [r.get('id') for r in cur.fetchall()]

    def save(self, data, table):
        conn = self.generate_conn()
        cur = conn.cursor() 

        for d in data:
            del d['server_act']
            f = str(tuple(str(x) for x in d)).replace("'", "")
            v = str(tuple(['%s']*len(d))).replace("'", "")
            sql = 'INSERT INTO %(name)s %(fields)s VALUES %(values)s'%{'name':table, 'fields': f, 'values':v}
            try:
                cur.execute(sql, d.values())
                conn.commit()
            except psycopg2.IntegrityError, e:
                fields = ", ".join(['%s = %s'%(f, "%s") for f in d])
                sql = "UPDATE %(name)s SET %(fields)s WHERE id = '%(id)s'"%{'name':table, 'fields': fields, 'id': d.get('id')}
                conn.rollback()
                cur.execute(sql, d.values())
                conn.commit()