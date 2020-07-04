class Changeset:
    """
    A changeset represents a series of changes that
    can be applied to the *database*.

    :param table: The TinyDB table.
    """

    def __init__(self, table):
        self.table = table
        self.record = []

    def execute(self):
        """
        Execute the changeset, applying every
        operation on the database. Note that this
        function is not idempotent, if you call
        it again and again it will be executed
        many times.
        """
        def updater(docs):
            for op in self.record:
                op.perform(docs)

        self.table._update_table(updater)
        self.table._next_id = None

    def append(self, change):
        """
        Append a *change* to the internal record
        of operations.

        :param change: The change to append.
        """
        self.record.append(change)
