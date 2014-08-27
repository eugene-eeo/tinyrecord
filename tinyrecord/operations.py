class Operation(object):
    def perform(self):
        raise NotImplementedError


class Insert(Operation):
    def __init__(self, document):
        self.document = document

    def perform(self, data):
        eid = max(data) if data else 0
        eid += 1
        data[eid] = self.document


class Update(Operation):
    def __init__(self, update, query):
        self.update = update
        self.query = query

    def perform(self, data):
        for key in data:
            value = data[key]
            if self.query(value):
                value.update(self.update)


class Remove(Operation):
    def __init__(self, query):
        self.query = query

    def perform(self, data):
        for key in list(data):
            value = data[key]
            if self.query(value):
                del data[key]
