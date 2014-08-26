from tinydb.database import Element


class Operation(object):
    def perform(self):
        raise NotImplementedError


class Insert(Operation):
    def __init__(self, document):
        self.document = document

    def perform(self, data):
        eid = sorted(data)[-1] if data else 0
        eid += 1
        data[eid] = Element(
            value=self.document,
            eid=eid,
        )


class Update(Operation):
    def __init__(self, update, query):
        self.update = update
        self.query = query

    def perform(self, data):
        for item in data:
            value = data[item]
            if self.query(value):
                value.update(self.update)


class Remove(Operation):
    def __init__(self, query):
        self.query = query

    def perform(self, data):
        for item in list(self.data):
            value = data[item]
            if self.query(value):
                del self.data[item]
