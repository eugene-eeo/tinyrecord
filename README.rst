::

    TinyDB __  _                                   __
          / /_(_)__  __ _________ _______  _______/ /
         / __/ / _ \/ // / __/ -_) __/ _ \/ __/ _  /
         \__/_/_//_/\_, /_/  \__/\__/\___/_/  \_,_/
                   /___/


**Supported Pythons:** 3.5+

Tinyrecord is a library which implements atomic
transaction support for the `TinyDB`_ NoSQL database.
It uses a record-first then execute architecture which
allows us to minimize the time that we are within a
thread lock. Usage example:

.. code-block:: python

    from tinydb import TinyDB, where
    from tinyrecord import transaction

    table = TinyDB('db.json').table('table')
    with transaction(table) as tr:
        # insert a new record
        tr.insert({'username': 'john'})
        # update records matching a query
        tr.update({'invalid': True}, where('username') == 'john')
        # delete records
        tr.remove(where('invalid') == True)
        # update using a function
        tr.update(updater, where(...))
        # insert many items
        tr.insert_multiple(documents)

Note that due to performance reasons you cannot view
the data within a transaction unless you've comitted.
You will have to call operations on the transaction
object and not the database itself. Since tinyrecord
works with dictionaries and the latest API, it will
only support the latest version (**4.x**).

Installation is as simple as ``pip install tinyrecord``.

.. image:: https://github.com/eugene-eeo/tinyrecord/actions/workflows/test.yml/badge.svg
    :target: https://github.com/eugene-eeo/tinyrecord/actions/workflows/test.yml
.. _TinyDB: https://github.com/msiemens/tinydb
