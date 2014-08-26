from threading import Thread
from tinydb.storages import MemoryStorage
from tinydb.database import TinyDB, Table
from tinyrecord import transaction, abort


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



def table(cls=FaultyTableRemove):
    class FaultyDB(TinyDB):
        def table(self, name='_default', **options):
            return cls(name, self, **options)

    db = FaultyDB(storage=MemoryStorage).table()
    return db


def test_transaction_abort():
    with transaction(None) as tr:
        abort()


def test_transaction_insert_faulty():
    db = table(FaultyTableInsert)
    try:
        with transaction(db) as tr:
            [tr.insert({}) for i in range(10)]
        raise AssertionError
    except ValueError:
        assert not db.all()


def test_transaction_insert():
    db = table()
    with transaction(db) as tr:
        tr.insert({})

    assert len(db.all()) == 1


def test_transaction_remove_faulty():
    db = table()
    [db.insert({}) for i in range(10)]
    try:
        with transaction(db) as tr:
            tr.remove(lambda x: True)
        raise AssertionError
    except ValueError:
        assert len(db.all()) == 10


def test_transaction_concurrent():
    db = table()

    def callback():
        with transaction(db) as tr:
            tr.insert({})

    threads = [Thread(target=callback) for i in range(5)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    ids = set(x.eid for x in db.all())
    assert len(ids) == 5
