import pytest
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage, JSONStorage
from tinyrecord import transaction, abort


@pytest.fixture(params=[
    MemoryStorage,
    JSONStorage,
])
def db(request, tmp_path):
    storage = request.param
    params = {'storage': storage}
    if storage is JSONStorage:
        params['path'] = str(tmp_path / "db.json")
    return TinyDB(**params)


def test_abort(db):
    db.table('test').insert_multiple([
        {"a": 1},
        {"b": 2},
        {"c": 3},
    ])
    data = db.storage.read().copy()

    with transaction(db) as db2:
        db2.table('test').remove(where('a') == 1)
        db2.table('test').remove(where('b') == 2)

        assert len(db2.table('test')) == 1
        assert db2.table('test').get(where('c') == 3) == {'c': 3}
        abort()

    assert db.storage.read() == data


def test_failed_txn(db):
    db.table('test').insert_multiple([
        {"a": 1},
        {"b": 2},
        {"c": 3},
    ])
    data = db.storage.read().copy()

    with pytest.raises(Exception):
        with transaction(db) as db2:
            db2.table('test').remove(where('a') == 1)
            db2.table('test').remove(where('b') == 2)
            raise Exception(1)

    assert db.storage.read() == data


def test_txn_create_tables(db):
    with transaction(db) as db2:
        db2.table('users').insert({'uid': 1})
        db2.table('users').insert({'uid': 2})

        a_id = db2.insert({'a': 1})
        b_id = db2.insert({'b': 2})

        assert db2.get(where('a') == 1) == {'a': 1}
        assert db2.get(where('a') == 1).doc_id == a_id
        assert db2.get(where('b') == 2).doc_id == b_id

    assert db.tables() == {db.default_table_name, 'users'}
    assert db.get(where('a') == 1).doc_id == a_id
    assert db.get(where('b') == 2).doc_id == b_id
    assert db.table('users').get(where('uid') == 1)
    assert db.table('users').get(where('uid') == 2)


def test_txn_flushes_query_cache(db):
    db.insert({'a': 1, 'x': 1})
    db.insert({'a': 1, 'x': 2})
    db.search(where('a') == 1)

    with transaction(db) as db2:
        db2.remove(where('x') == 2)

    assert db.search(where('a') == 1) == [{'a': 1, 'x': 1}]
