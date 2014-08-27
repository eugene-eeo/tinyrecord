from functools import wraps
from threading import Lock
from tinyrecord.changeset import Changeset
from tinyrecord.operations import (Insert, Remove,
                                   Update, InsertMultiple)


def records(cls):
    """
    Helper method for creating a method that records
    another operation to the changeset.

    :param cls: The operation class.
    """
    @wraps(cls)
    def proxy(self, *args, **kwargs):
        self.record.append(cls(*args, **kwargs))
    return proxy


class AbortSignal(Exception):
    """
    Signals the abortion of a transaction. It is
    ignored when raised within the body of a
    transaction.
    """
    pass


class transaction(object):
    """
    Create an atomic transaction for the given
    *table*. All IO actions during the transaction are
    executed within a lock.

    :param table: The TinyDB table.
    """

    def __init__(self, table):
        self.lock = Lock()
        self.record = Changeset(table)

    update = records(Update)
    insert = records(Insert)
    insert_multiple = records(InsertMultiple)
    remove = records(Remove)

    def __enter__(self):
        """
        Enter a transaction.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Commits the transaction and raises a traceback
        if it is not an ``AbortSignal``. All actions
        are executed within a lock.
        """
        if not traceback:
            with self.lock:
                self.record.execute()
        self.record.clear()
        return isinstance(value, AbortSignal)
