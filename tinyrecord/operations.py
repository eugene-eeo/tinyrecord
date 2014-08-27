class Operation(object):
    def perform(self):
        raise NotImplementedError


class InsertMultiple(Operation):
    def __init__(self, iterable):
        self.iterable = iterable

    def perform(self, data):
        eid = max(data) if data else 0
        for element in self.iterable:
            eid += 1
            data[eid] = element


class Insert(Operation):
    def __new__(self, element):
        return InsertMultiple((element,))


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
