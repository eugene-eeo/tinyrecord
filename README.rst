::

    TinyDB __  _                                   __
          / /_(_)__  __ _________ _______  _______/ /
         / __/ / _ \/ // / __/ -_) __/ _ \/ __/ _  /
         \__/_/_//_/\_, /_/  \__/\__/\___/_/  \_,_/
                   /___/


**Supported Pythons:** 3.5+

Tinyrecord is a library which implements atomic
transaction support for the `TinyDB`_ NoSQL database.
The supported version is **4.x**:

.. code-block:: python

    from tinydb import TinyDB, where
    from tinyrecord import transaction

    real_db = TinyDB('db.json')
    with transaction(real_db) as db:
        # use db as you would normally use TinyDB
        users = db.table('users')
        users.insert({'uid': 1, 'name': '...'})
        # read within the transaction
        doc = users.get(where('uid') == 1)
        assert doc['uid'] == 1

    real_db.table('users').get(where('uid') == 1)

Installation is as simple as ``pip install tinyrecord``.

.. image:: https://travis-ci.org/eugene-eeo/tinyrecord.svg?branch=master
    :target: https://travis-ci.org/eugene-eeo/tinyrecord
.. _TinyDB: https://github.com/msiemens/tinydb
