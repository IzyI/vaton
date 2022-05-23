import asyncio
from functools import wraps


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )


def read_file_content(path, mode="r"):
    with open(path, mode) as _f:
        content = _f.read()
    return content


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
