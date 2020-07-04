"""
    tinyrecord
    ~~~~~~~~~~

    Implements atomic transaction support for the
    embedded TinyDB NoSQL database.

    :copyright: (c) 2020 by Eeo Jun.
    :license: MIT, see LICENSE for more details.
"""

import copy
from contextlib import contextmanager
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


__all__ = ('transaction', 'abort')


class AbortTransaction(Exception):
    pass


def abort():
    raise AbortTransaction


@contextmanager
def null_lock():
    yield


@contextmanager
def transaction(db, lock=None):
    """
    Begin a transaction on the TinyDB database *db*.
    For locking support, you can provide a custom *lock*,
    e.g. `threading.Lock()` which would be held when
    the transaction is executing.

    :param db: `TinyDB` database.
    :param lock: Lock to hold (defaults to a no-op).
    """
    lock = null_lock() if lock is None else lock
    with lock:
        data = copy.deepcopy(db.storage.read())
        tmp_db = TinyDB(storage=MemoryStorage)
        tmp_db.table_class = db.table_class
        tmp_db.storage.write(data)
        try:
            yield tmp_db

            db.storage.write(tmp_db.storage.read())
            for item in tmp_db.tables():
                db.table(item).clear_cache()
            del data

        except AbortTransaction:
            pass
