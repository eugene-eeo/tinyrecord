from contextlib import contextmanager


class Changeset(object):
    def __init__(self, database):
        self.db = database
        self.record = []

    def __iter__(self):
        for item in self.record:
            yield item

    @property
    @contextmanager
    def data(self):
        data = self.db._read()
        yield data
        self.db._write(data)
        if not data:
            return
        last_id = max(data)
        self.db._last_id = max((last_id, self.db._last_id))

    def execute(self):
        with self.data as data:
            for operation in self.record:
                operation.perform(data)

    def append(self, change):
        self.record.append(change)

    def clear(self):
        del self.record[:]
