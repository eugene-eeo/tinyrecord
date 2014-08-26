from threading import Lock
from tinyrecord.operations import Insert, Remove


class AbortSignal(Exception):
    pass


def records(op_cls):
    def proxy(self, document):
        op = op_cls(self.table, document)
        self.record.append(op)
    return proxy


class transaction(object):
    def __init__(self, table):
        self.lock = Lock()
        self.table = table
        self.record = []

    def clear(self):
        del self.record[:]

    insert = records(Insert)
    remove = records(Remove)

    def undo(self, upto):
        history = self.record[:upto]
        for item in reversed(history):
            item.undo()

    def execute(self):
        for index, operation in enumerate(self.record):
            try:
                operation.perform()
            except:
                self.undo(upto=index)
                operation.undo()
                raise

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not traceback:
            with self.lock:
                self.execute()
        self.clear()
        return isinstance(value, AbortSignal)
