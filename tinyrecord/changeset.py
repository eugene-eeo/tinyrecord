class Changeset(object):
    """
    A changeset represents a series of changes that
    can be applied to the *database*.

    :param database: The TinyDB table.
    """

    def __init__(self, database):
        self.db = database
        self.record = []

    def execute(self):
        """
        Execute the changeset, applying every
        operation on the database. Note that this
        function is not idempotent, if you call
        it again and again it will be executed
        many times.
        """
        data = self.db._read()
        for operation in self.record:
            operation.perform(data)
        self.db._write(data)
        self.db.clear_cache()
        self.db._last_id = max(
            max(data) if data else -1,
            self.db._last_id,
        )

    def append(self, change):
        """
        Append a *change* to the internal record
        of operations.

        :param change: The change to append.
        """
        self.record.append(change)
