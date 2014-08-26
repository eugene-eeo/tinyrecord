::

    TinyDB __  _                                   __
          / /_(_)__  __ _________ _______  _______/ /
         / __/ / _ \/ // / __/ -_) __/ _ \/ __/ _  /
         \__/_/_//_/\_, /_/  \__/\__/\___/_/  \_,_/
                   /___/


Tinyrecord is a library which implements experimental
transaction support for the `TinyDB`_ NoSQL database.
Usage example:

.. code-block:: python

    from tinydb import TinyDB, where
    from tinyrecord import transaction

    table = TinyDB('db.json').table('table')
    with transaction(table) as tr:
        tr.insert({})
        tr.remove(where('x') == 'y')


.. _TinyDB: https://github.com/msiemens/tinydb
