
class DatabaseManagerClientBase():
    def generate_conn(self, config = None):
        raise NotImplemented()

    def query(self, table, limit=None, offset=None):
        raise NotImplemented()

    def query_sync(self, table, limit=None, offset=None):
        raise NotImplemented()

    def insert(self, data, table):
        raise NotImplemented()

    def update(self, data, table):
        raise NotImplemented()
