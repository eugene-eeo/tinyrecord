class Changeset(object):
    def __init__(self, database):
        self.db = database
        self.record = []

    def execute(self):
        data = self.db._read()
        for operation in self.record:
            operation.perform(data)
        self.db._write(data)
        if data:
            last_id = max(data)
            db_last = self.db._last_id
            if db_last < last_id:
                self.db._last_id = last_id

    def append(self, change):
        self.record.append(change)

    def clear(self):
        del self.record[:]
