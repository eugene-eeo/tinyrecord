from pytest import fixture
from threading import Thread
from tinydb import where, TinyDB
from tinydb.storages import MemoryStorage
from tinyrecord import transaction, abort


@fixture
def db():
    return TinyDB(storage=MemoryStorage).table()


def test_update(db):
    db.insert({'x': 1})

    with transaction(db) as tr:
        tr.update({'x': 2}, where('x') == 1)

    assert db.get(where('x') == 2)


def test_atomicity(db):
    try:
        with transaction(db) as tr:
            tr.insert({})
            raise ValueError
        raise AssertionError
    except ValueError:
        assert not db.all()


def test_abort(db):
    with transaction(db) as tr:
        tr.insert({})
        abort()

    assert not db.all()


def test_insert(db):
    with transaction(db) as tr:
        tr.insert({})

    assert len(db.all()) == 1
    assert db._last_id == 1


def test_concurrent(db):
    def callback():
        with transaction(db) as tr:
            tr.insert({})

    threads = [Thread(target=callback) for i in range(5)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    ids = set(x.eid for x in db.all())
    assert len(ids) == 5
