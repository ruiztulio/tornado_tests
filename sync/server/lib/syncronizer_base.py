
class SyncronizerBase():
    _dm = None

    def __init__(self, dm):
        self._dm = dm()


    def sync_this(self, data, table):
        updates = self._dm.get_updated(data, table)
        #deletes = self._dm.get_deleted(data)
        uploads = self._dm.get_uploads(data, table)
        return {'updates': updates, 'uploads': uploads}

    def sync(self, data, table):
        #res = self.sync_this(data, table)
        updates = self._dm.get_updated(data, table)
        uploads = self._dm.get_full_uploads(data, table)
        inserts = self._dm.get_inserts(data, table)
        print "Sync"
        print "Inserts ", inserts
        return {'updates': updates, 'uploads': uploads, 'inserts': inserts}