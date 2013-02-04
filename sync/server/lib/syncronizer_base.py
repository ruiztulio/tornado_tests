
class SyncronizerBase():
    """
    Esta clase contiene los algoritmos para la sincronizacion 
    invocando los metodos correspondientes del gestor de base de datos,
    a diferencia de las otras clases base esta tiene los metodos implementados
    en vista de que solo hace uso de la interfaz de DatabaseManagerBase
    si se desea cambiar el algoritmo o implementar otro se sobrecargan
    los metodos pertinentes
    """
    _dm = None

    def __init__(self, dm):
        """
        Constuctor de la clase 

        Args:
            dm (DatabaseManagerBase): Implementacion de DatabaseManagerBase segun el motor de base de datos que se quiera usar

        """

        self._dm = dm()


    def sync_this(self, data, table):
        """
        Sincroniza unicamente la informacion que se pasa en el parametro data en la tabla indicada,
        este metodo es util en caso de que el cliente desee sincronizar por partes, 
        no se retornan los inserts

        Args:
            data (list): Lista de diccionarios con los ids y timestamps de los registros que se desean Sincronizar

            table (str): Nombre de la tabla con la se desea sincronizar los tegistros contenidos en data
        """
        updates = self._dm.get_updated(data, table)
        #deletes = self._dm.get_deleted(data)
        uploads = self._dm.get_uploads(data, table)
        return {'updates': updates, 'uploads': uploads}

    def sync(self, data, table):
        """
        Sincroniza la informacion que se pasa en el parametro data en la tabla indicada,
        este metodo es util en caso de que el cliente desee sincronizar por partes, 
        se retorna toda la informacin necesaria para la sincronizacion

        Args:
            data (list): Lista de diccionarios con los ids y timestamps de los registros que se desean Sincronizar

            table (str): Nombre de la tabla con la se desea sincronizar los tegistros contenidos en data
        """
        updates = self._dm.get_updated(data, table)
        uploads = self._dm.get_full_uploads(data, table)
        inserts = self._dm.get_inserts(data, table)
        print "Sync"
        print "Inserts ", inserts
        return {'updates': updates, 'uploads': uploads, 'inserts': inserts}
