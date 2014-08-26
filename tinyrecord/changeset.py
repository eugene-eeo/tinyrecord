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
            self.db._last_id = sorted(data)[-1]

    def append(self, change):
        self.record.append(change)

    def clear(self):
        del self.record[:]
