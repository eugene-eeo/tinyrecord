from threading import Lock
from tinytransaction.operations import Insert, Remove


class AbortSignal(Exception):
    pass


def records(op_cls):
    def proxy(self, document):
        op = op_cls(self.table, document)
        self.record.append(op)
    return proxy


class Transaction(object):
    def __init__(self, table):
        self.lock = Lock()
        self.table = table
        self.record = []

    def clear(self):
        del self.record[:]

    insert = records(Insert)
    remove = records(Remove)

    def execute(self):
        for index, operation in enumerate(self.record):
            try:
                operation.perform()
            except:
                history = self.record[:index]
                for item in reversed(history):
                    item.undo()
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
