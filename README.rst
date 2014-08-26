::

    TinyDB __  _                                   __
          / /_(_)__  __ _________ _______  _______/ /
         / __/ / _ \/ // / __/ -_) __/ _ \/ __/ _  /
         \__/_/_//_/\_, /_/  \__/\__/\___/_/  \_,_/
                   /___/


**Supported Pythons:** 2.6+, 3.2+

Tinyrecord is a library which implements experimental
atomic transaction support for the `TinyDB`_ NoSQL
database. It uses a record-first then execute architecture
which allows us to minimize the time that we are within
a thread lock. Usage example:

.. code-block:: python

    from tinydb import TinyDB, where
    from tinyrecord import transaction

    table = TinyDB('db.json').table('table')
    with transaction(table) as tr:
        tr.insert({})
        tr.remove(where('x') == 'y')

Note that you will have to call operations on the
transaction object and not the database itself. Since
tinyrecord requires some ID madness for keeping track
of records deleted and inserted, it will only work
with the latest development version (**2.0**).

.. _TinyDB: https://github.com/msiemens/tinydb
