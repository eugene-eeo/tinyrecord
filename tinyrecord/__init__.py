from tinyrecord.transaction import transaction, AbortSignal
__all__ = ('transaction', 'abort')


def abort():
    """
    Aborts the transaction. All operations defined on
    the transaction will be ignored (discarded).
    Raises the ``AbortSignal``, to be called only
    within a transaction.
    """
    raise AbortSignal
