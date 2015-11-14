from pytest import fixture, raises
from threading import Thread
from tinydb import where, TinyDB
from tinydb.storages import MemoryStorage
from tinyrecord import transaction, abort


@fixture
def db():
    return TinyDB(storage=MemoryStorage).table()


def test_insert_multiple(db):
    with transaction(db) as tr:
        tr.insert_multiple({} for x in range(5))

    assert len(db) == 5


def test_update_callable(db):
    [db.insert({'x': {'u': 10}}) for i in range(5)]

    with transaction(db) as tr:
        def function(t):
            t['x']['u'] = 1
        tr.update_callable(function, lambda x: True)

    assert len(db) == 5
    assert all(x['x']['u'] == 1 for x in db.search(lambda x: True))


def test_remove(db):
    [db.insert({}) for i in range(10)]
    anything = lambda x: True
    db.search(anything)

    with transaction(db) as tr:
        tr.remove(anything)

    assert not db._query_cache
    assert len(db) == 0

    db.insert({})
    assert db.get(anything).eid == 11


def test_remove_eids(db):
    eid = db.insert({'x': 1})

    with transaction(db) as tr:
        tr.remove(eids=[eid])

    assert not db.get(eid=eid)


def test_update(db):
    eid = db.insert({'x': 1})

    with transaction(db) as tr:
        tr.update({'x': 2}, where('x') == 1)
        tr.update({'x': 3}, eids=[eid])

    assert db.get(where('x') == 3).eid == eid


def test_atomicity(db):
    with raises(ValueError):
        with transaction(db) as tr:
            tr.insert({})
            tr.insert({'x': 1})
            tr.update({'x': 2}, where('x') == 1)
            raise ValueError
    assert len(db) == 0


def test_abort(db):
    with transaction(db) as tr:
        tr.insert({})
        abort()

    assert len(db) == 0


def test_insert(db):
    with transaction(db) as tr:
        tr.insert({})

    assert len(db) == 1
    assert db._last_id == 1


def test_concurrent(db):
    def callback():
        with transaction(db) as tr:
            tr.insert({})
            tr.insert({})

    threads = [Thread(target=callback) for i in range(10)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    ids = set(x.eid for x in db.all())
    assert len(ids) == 20
