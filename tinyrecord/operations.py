from typing import Any, Callable, Dict, Iterable, Optional

QueryFunction = Callable[[Any], bool]


class Operation:
    """
    An operation represents a single, atomic
    sequence of things to do to in-memory data.
    Every operation must implement the abstract
    ``perform`` method.
    """
    def perform(self, data: Dict[int, Any]) -> None:
        raise NotImplementedError


class InsertMultiple(Operation):
    """
    Insert multiple records *iterable* into the
    database.

    :param iterable: The iterable of elements to
        be inserted into the DB.
    """
    def __init__(self, iterable: Iterable[Any]) -> None:
        self.iterable = iterable

    def perform(self, data: Dict[int, Any]) -> None:
        doc_id = max(data) if data else 0
        for element in self.iterable:
            doc_id += 1
            data[doc_id] = element


class Update(Operation):
    """
    Mutate each of the records with a given
    *function* for all records that match a
    certain *query* (if specified). If *doc_ids*
    is specified, then the update is performed
    over those which have doc_id in *doc_ids*.

    :param function: Updator function, or a dictionary
                     of fields to update.
    :param query:    Query function.
    :param doc_ids:  Iterable of document IDs.
    """
    def __init__(
        self,
        function: Callable[[Any], Any],
        query: Optional[QueryFunction] = None,
        doc_ids: Optional[Iterable[int]] = None
    ) -> None:
        if query is None and doc_ids is None:
            raise TypeError("query or doc_ids must be specified")
        self.function = function if callable(function) else \
                        lambda x: x.update(function)
        self.query = query
        self.doc_ids = doc_ids

    def perform(self, data: Dict[int, Any]) -> None:
        if self.query is not None:
            for key in data:
                value = data[key]
                if self.query(value):
                    self.function(value)
        else:
            assert self.doc_ids is not None
            for key, value in data.items():
                if key in self.doc_ids:
                    self.function(value)


class Remove(Operation):
    """
    Remove documents from the DB matching
    the given *query*, or alternatively if
    *doc_ids* is specified, then those which
    have the given doc_ids.

    :param query: Query.
    :param doc_ids: Document ids.
    """
    def __init__(
        self,
        query: Optional[QueryFunction] = None,
        doc_ids: Optional[Iterable[int]] = None
    ) -> None:
        if query is None and doc_ids is None:
            raise TypeError("query or doc_ids must be specified")
        self.query = query
        self.doc_ids = set(doc_ids) if doc_ids is not None else None

    def perform(self, data: Dict[int, Any]) -> None:
        if self.query is not None:
            for key in list(data):
                if self.query(data[key]):
                    del data[key]
        else:
            assert self.doc_ids is not None
            for key in self.doc_ids:
                data.pop(key)
