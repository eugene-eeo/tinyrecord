from functools import update_wrapper
from threading import RLock
from tinyrecord.changeset import Changeset
from tinyrecord.operations import (Remove,
                                   InsertMultiple,
                                   UpdateCallable,
                                   null_query)


class AbortSignal(Exception):
    """
    Signals the abortion of a transaction. It is
    ignored when raised within the body of a
    transaction.
    """
    pass


def abort():
    """
    Aborts the transaction. All operations defined on
    the transaction will be ignored (discarded).
    Raises the ``AbortSignal``, to be called only
    within a transaction.
    """
    raise AbortSignal


def records(cls):
    """
    Helper method for creating a method that records
    another operation to the changeset.

    :param cls: The operation class.
    """
    def proxy(self, *args, **kwargs):
        self.record.append(cls(*args, **kwargs))
    update_wrapper(proxy, cls)
    return proxy


class transaction(object):
    """
    Create an atomic transaction for the given
    *table*. All IO actions during the transaction are
    executed within a lock.

    :param table: The TinyDB table.
    """

    def __init__(self, table):
        self.lock = RLock()
        self.record = Changeset(table)

    update_callable = records(UpdateCallable)
    insert_multiple = records(InsertMultiple)
    remove = records(Remove)

    def insert(self, row):
        return self.insert_multiple((row,))

    def update(self, fields, query=null_query, eids=[]):
        updator = lambda doc: doc.update(fields)
        return self.update_callable(updator, query, eids)

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
        if not traceback and self.record.has_ops:
            with self.lock:
                self.record.execute()
                self.record.clear()
        return isinstance(value, AbortSignal)
