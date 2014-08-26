from tinydb.storages import MemoryStorage
from tinydb.database import TinyDB, Table
from tinytransaction import transaction, abort


class FaultyTableRemove(Table):
    def remove(self, *args, **kwargs):
        raise ValueError


class FaultyTableInsert(Table):
    runs = 0

    def insert(self, *args, **kwargs):
        self.runs += 1
        if self.runs > 2:
            raise ValueError
        return super(FaultyTableInsert, self).insert(*args, **kwargs)



def table(cls=FaultyTableRemove, insert=True):
    class FaultyDB(TinyDB):
        def table(self, name='_default', **options):
            return cls(name, self, **options)

    db = FaultyDB(storage=MemoryStorage).table()
    if insert:
        [db.insert({}) for i in range(10)]
    return db


def test_transaction_abort():
    with transaction(None) as tr:
        abort()


def test_transaction_insert_faulty():
    db = table(FaultyTableInsert, insert=False)
    try:
        with transaction(db) as tr:
            for i in range(10):
                tr.insert({})
        raise AssertionError
    except ValueError:
        assert not db.all()


def test_transaction_insert():
    db = table()
    with transaction(db) as tr:
        tr.insert({})

    assert len(db.all()) == 11


def test_transaction_remove():
    db = table()
    try:
        with transaction(db) as tr:
            tr.remove(lambda x: True)
        raise AssertionError
    except ValueError:
        assert len(db.all()) == 10
