#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        """
        Este metodo es usado para obtener los registros que se han modificado 
        en el servidor

        Args:
            data (list): lista de diccionarios con los ids y los timestamp 
                de los registros que se quieren sincronizar

            table (str): nombre de la tabla con la que se quiere hacer 
                la sincronizacion en el servidor

        Returns:
            La lista de ids de los registris que se le solicitaran al cliente
            
        """
        raise NotImplemented()

    def get_uploads(self, data, table):
        """
        Retorda todos los registros que deben ser actualizados en el servidor
        tomando únicamente en cuenta los registros que se pasan por en parametro
        data, no se solicitan los nuevos registros, unicamente los actualizados

        Args:
            data (list): lista de diccionarios con los ids y los timestamp 
                de los registros que se quieren sincronizar

            table (str): nombre de la tabla con la que se quiere hacer 
                la sincronizacion en el servidor

        Returns:
            La lista de ids de los registros que han sido modificados del lado del servidor

            
        """
        raise NotImplemented()

    def get_full_uploads(self, data, table):
        """
        Retorna todos los registros que deben ser actualizados en el servidor 
        ya sean nuevos registros o actualizaciones

        Args:
            data (list): lista de diccionarios con los ids y los timestamp 
                de los registros que se quieren sincronizar

            table (str): nombre de la tabla con la que se quiere hacer 
                la sincronizacion en el servidor

        Returns:
            La lista de ids de los registris que se le solicitaran al cliente
        """
        raise NotImplemented()

    def save(self, data, table):
        """
        Este metodo guarda (insert y update segun corresponda) los registros 
        que se le pasan en data en forma de una lista de diccionarios

        Args:
            data (list): lista de diccionarios con la informacion que se desea guardar

            table (str): nombre de la tabla en la que se guardaran los registros

        """
        raise NotImplemented()

