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

    @contextmanager
    def observed(self):
        """
        Returns the data from reading the database
        for mutation and writes the data to the
        database on exit.
        """
        data = self.db._read()
        yield data
        self.db._write(data)
        self.db.clear_cache()
        if data:
            self.db._last_id = max(
                max(data),
                self.db._last_id,
            )

    def execute(self):
        """
        Execute the changeset, applying every
        operation on the database. Note that this
        function is not idempotent, if you call
        it again and again it will be executed
        many times.
        """
        with self.observed() as data:
            for operation in self.record:
                operation.perform(data)

    def append(self, change):
        """
        Append a *change* to the internal record
        of operations.

        :param change: The change to append.
        """
        self.record.append(change)
