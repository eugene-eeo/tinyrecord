class Operation(object):
    def perform(self):
        raise NotImplementedError


class InsertMultiple(Operation):
    """
    Insert multiple records *iterable* into the
    database.

    :param iterable: The iterable of elements to
        be inserted into the DB.
    """
    def __init__(self, iterable):
        self.iterable = iterable

    def perform(self, data):
        eid = max(data) if data else 0
        for element in self.iterable:
            eid += 1
            data[eid] = element


class Insert(Operation):
    """
    Insert a single record into the database.
    An insert is just a special case of the
    ``InsertMultiple`` where you insert a
    one element tuple of the element.

    :param element: The element to insert.
    """
    def __new__(self, element):
        return InsertMultiple((element,))


class Update(Operation):
    """
    Update the records in the database that
    match a certian *query* with the *fields*.

    :param fields: The fields to update.
    :param query: Update all documents
        matching this query.
    """
    def __init__(self, fields, query):
        self.fields = fields
        self.query = query

    def perform(self, data):
        for key in data:
            value = data[key]
            if self.query(value):
                value.update(self.fields)


class Remove(Operation):
    """
    Remove documents from the DB matching
    the given *query*.

    :param query: The query to remove.
    """
    def __init__(self, query):
        self.query = query

    def perform(self, data):
        for key in list(data):
            value = data[key]
            if self.query(value):
                del data[key]
