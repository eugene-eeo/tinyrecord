tinytransaction
===============

Implements experimental transaction support for the
`TinyDB`_ NoSQL database. Usage example:

.. code-block:: python

    from tinydb import TinyDB, where
    from tinytransaction import transaction

    table = TinyDB('db.json').table('table')
    with transaction(table) as tr:
        tr.insert({})
        tr.remove(where('x') == 'y')


.. _TinyDB: https://github.com/msiemens/tinydb
