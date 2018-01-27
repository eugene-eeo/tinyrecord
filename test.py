import threading
from tinydb import TinyDB, where
from tinyrecord import transaction

db = TinyDB('db.json')
db.purge()
table = db.table('settings')
table.insert({'name': 'test', 'value': 0})

def increment_values():
    for i in range(100):
        with transaction(table) as tr:
            def f(doc):
                doc['value'] += 1
            tr.update_callable(f, where('name') == 'test')


threads = [threading.Thread(target=increment_values) for _ in range(2)]
[t.start() for t in threads]
[t.join() for t in threads]
db.all()
