from functools import wraps
from threading import Lock
from types import TracebackType
from typing import Any, Callable, MutableMapping, NoReturn, Optional, Type
from weakref import WeakKeyDictionary

from tinydb.table import Table

from tinyrecord.changeset import Changeset
from tinyrecord.operations import (Operation,
                                   Remove,
                                   InsertMultiple,
                                   Update)


class AbortSignal(Exception):
    """
    Signals the abortion of a transaction. It is
    ignored when raised within the body of a
    transaction.
    """
    pass


def abort() -> NoReturn:
    """
    Aborts the transaction. All operations defined on
    the transaction will be ignored (discarded).
    Raises the ``AbortSignal``, to be called only
    within a transaction.
    """
    raise AbortSignal


def records(cls: Type[Operation]) -> Callable[..., None]:
    """
    Helper method for creating a method that records
    another operation to the changeset.

    :param cls: The operation class.
    """
    @wraps(cls)
    def proxy(self: "transaction", *args: Any, **kwargs: Any) -> None:
        # Too many arguments for "Operation"
        self.record.append(cls(*args, **kwargs))  # type: ignore[call-arg]
    return proxy


class transaction:
    """
    Create an atomic transaction for the given
    *table*. All IO actions during the transaction are
    executed within a database-local lock.

    :param table: A TinyDB table.
    """

    _locks: MutableMapping[Table, Lock] = WeakKeyDictionary()

    def __init__(self, table: Table) -> None:
        self.record = Changeset(table)
        self.lock = (self._locks.get(table) or
                     self._locks.setdefault(table, Lock()))

    insert_multiple = records(InsertMultiple)
    update = records(Update)
    remove = records(Remove)

    def insert(self, row: Any) -> None:
        self.insert_multiple((row,))

    def __enter__(self) -> "transaction":
        """
        Enter a transaction.
        """
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> bool:
        """
        Commits the transaction and raises a traceback
        if it is not an ``AbortSignal``. All actions
        are executed within a lock.
        """
        if not traceback:
            with self.lock:
                self.record.execute()
        return isinstance(value, AbortSignal)
