from contextlib import contextmanager


class Changeset(object):
    """
    A changeset represents a series of changes that
    can be applied to the *database*.

    :param database: The TinyDB table.
    """

    def __init__(self, database):
        self.db = database
        self.record = []

    @property
    @contextmanager
    def data(self):
        """
        Returns the data from reading the database
        and updates the database's last_id properly,
        as well as clearing the cache on exit.
        """
        data = self.db._read()
        yield data
        self.db._write(data)
        self.db._query_cache.clear()
        if data:
            d1, d2 = max(data), self.db._last_id
            self.db._last_id = d1 if d1 > d2 else d2

    def execute(self):
        """
        Execute the changeset, applying every
        operation on the database. Note that this
        function is not idempotent, if you call
        it again and again it will be executed
        many times.
        """
        with self.data as data:
            for operation in self.record:
                operation.perform(data)

    def append(self, change):
        """
        Append a *change* to the internal record
        of operations.

        :param change: The change to append.
        """
        self.record.append(change)

    def clear(self):
        """
        Clear the internal record.
        """
        self.record = []
