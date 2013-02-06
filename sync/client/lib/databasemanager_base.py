
class DatabaseManagerClientBase():
    """
    Las implementaciones de las clases para manejar la sincronizacion del lado del cliente deben heredar
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

    def query(self, table, ids=None, limit=None, offset=None):
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

    def insert(self, data, table, gen_id=False, gen_write_date=False):
        """
        Inserta el registro contenido en data en la tabla indicada

        Args:
            data (dict): diccionario con el registro a insertar

            table (str): nombre de la tabla en la que se insertaran los registros

        Kwargs:
            gen_id (bool): Si se desea que la aplicacion genere el id del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

            gen_write_date (bool): Si se desea que la aplicacion genere el timestamp del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos
                
        Returns:
            El id del registro insertado
        """
        raise NotImplemented()

    def insert_many(self, data, table, gen_id=False, gen_write_date=False):
        """
        Inserta los registros contenidos en data en la tabla indicada

        Args:
            data (list): lista de diccionarios con el registros a insertar

            table (str): nombre de la tabla en la que se insertaran los registros

        Kwargs:
            gen_id (bool): Si se desea que la aplicacion genere el id del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

            gen_write_date (bool): Si se desea que la aplicacion genere el timestamp del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

        Returns:
            Una lista con los ids de los registros insertados
        """
        raise NotImplemented()

    def update(self, data, table):
        """
        Actualiza el registro contenido en data en la tabla indicada

        Args:
            data (dict): diccionario con el registro a actualizar,
                el diccionario debe contenr el id del registro

            table (str): nombre de la tabla en la que se insertaran los registros

        Kwargs:
            gen_id (bool): Si se desea que la aplicacion genere el id del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

            gen_write_date (bool): Si se desea que la aplicacion genere el timestamp del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

        Returns:
            El id del registro actualizado o falso en caso negativo
        """
        raise NotImplemented()

    def update_many(self, data, table):
        """
        Actualiza los registros contenidos en data en la tabla indicada

        Args:
            data (list): lista de diccionarios con los registros a insertar,
                cada diccionario debe contener el id del registro que acrualizara

            table (str): nombre de la tabla en la que se insertaran los registros

        Kwargs:
            gen_id (bool): Si se desea que la aplicacion genere el id del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

            gen_write_date (bool): Si se desea que la aplicacion genere el timestamp del registro,
                por defecto es falso, lo que implica que este trabajo lo hara en motor de base de datos

        Returns:
            El id del registro actualizado o falso en caso negativo
        """
        raise NotImplemented()

