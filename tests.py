from threading import Thread
from tinydb import where
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
        super(FaultyTableInsert, self).insert(*args, **kwargs)
        if self.runs > 2:
            raise ValueError


class FaultyTableUpdate(Table):
    runs = 0

    def update(self, *args, **kwargs):
        super(FaultyTableUpdate, self).update(*args, **kwargs)
        raise ValueError


def table(cls=Table):
    class FaultyDB(TinyDB):
        def table(self, name, **options):
            return cls(name, self, **options)

    db = FaultyDB(storage=MemoryStorage)
    return db.table('default_')



def test_transaction_update():
    db = table()
    db.insert({'x': 1})

    with transaction(db) as tr:
        tr.update({'x': 2}, where('x') == 1)

    assert db.get(where('x') == 2)


def test_transaction_abort():
    with transaction(None) as tr:
        abort()


def test_transaction_insert():
    db = table()
    with transaction(db) as tr:
        tr.insert({})

    assert len(db.all()) == 1


def test_transaction_update_faulty():
    db = table(FaultyTableUpdate)
    db.insert_multiple({'x': 1} for x in range(10))
    try:
        with transaction(db) as tr:
            tr.update({'x': 2}, lambda x: True)
        raise AssertionError
    except ValueError:
        for item in (d['x'] for d in db.all()):
            assert item == 1


def test_transaction_insert_faulty():
    db = table(FaultyTableInsert)
    try:
        with transaction(db) as tr:
            [tr.insert({}) for i in range(10)]
        raise AssertionError
    except ValueError:
        assert not db.all()


def test_transaction_remove_faulty():
    db = table(FaultyTableRemove)
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
