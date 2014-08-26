from functools import partial
from operator import eq


class Insert(object):
    def __init__(self, db, document):
        self.document = document
        self.eid = -1
        self.db = db

    def perform(self):
        self.db.insert(self.document)
        self.eid = self.db._last_id

    def undo(self):
        self.db.remove(lambda x: x.eid == self.eid)


class Remove(object):
    def __init__(self, db, query):
        self.query = query
        self.deleted = []
        self.db = db

    def perform(self):
        self.deleted = self.db.search(self.query)
        self.db.remove(self.query)

    def undo(self):
        data = self.db._read()
        for item in self.deleted:
            data[item.eid] = item
        self.db._write(data)
