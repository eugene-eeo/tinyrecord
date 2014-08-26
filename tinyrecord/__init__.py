from tinyrecord.transaction import Transaction, AbortSignal

__all__ = ('transaction', 'abort')
transaction = Transaction


def abort():
    raise AbortSignal
