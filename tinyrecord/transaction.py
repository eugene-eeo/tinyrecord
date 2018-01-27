from functools import wraps
from threading import Lock
from weakref import WeakKeyDictionary
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
    @wraps(cls)
    def proxy(self, *args, **kwargs):
        self.record.append(cls(*args, **kwargs))
    return proxy


class transaction(object):
    """
    Create an atomic transaction for the given
    *table*. All IO actions during the transaction are
    executed within a database-local lock.

    :param table: A TinyDB table.
    """

    _locks = WeakKeyDictionary()

    def __init__(self, table):
        self.record = Changeset(table)
        self.lock = (self._locks.get(table) or
                     self._locks.setdefault(table, Lock()))

    update_callable = records(UpdateCallable)
    insert_multiple = records(InsertMultiple)
    remove = records(Remove)

    def insert(self, row):
        return self.insert_multiple((row,))

    def update(self, fields, query=null_query, doc_ids=[], eids=[]):
        updator = lambda doc: doc.update(fields)
        if eids and doc_ids:
            raise TypeError('cannot pass both eids and doc_ids')
        return self.update_callable(updator, query, doc_ids, eids)

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
        return isinstance(value, AbortSignal)
