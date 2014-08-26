from tinyrecord.transaction import transaction, AbortSignal
__all__ = ('transaction', 'abort')


def abort():
    raise AbortSignal
