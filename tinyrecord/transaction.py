from threading import Lock
from tinyrecord.changeset import Changeset
from tinyrecord.operations import Insert, Remove, Update


def records(op_cls):
    def proxy(self, *args, **kwargs):
        op = op_cls(*args, **kwargs)
        self.record.append(op)
    return proxy


class AbortSignal(Exception):
    pass


class transaction(object):
    def __init__(self, table):
        self.lock = Lock()
        self.record = Changeset(table)

    update = records(Update)
    insert = records(Insert)
    remove = records(Remove)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not traceback:
            with self.lock:
                self.record.execute()
        self.record.clear()
        return isinstance(value, AbortSignal)
