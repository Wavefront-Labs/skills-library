---
id: computing-software.software-engineering.python.writing-decorators-with-functools-wraps
name: writing-decorators-with-functools-wraps
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, python-decorators, functools-wraps, paramspec, closures, higher-order-functions]
level: practitioner
status: verified
description: "Write correct decorators: functools.wraps, decorators with arguments, preserving signatures for type checkers with ParamSpec, async support and class decorators."
sources:
  - https://docs.python.org/3/library/functools.html#functools.wraps
  - https://docs.python.org/3/glossary.html#term-decorator
  - https://peps.python.org/pep-0612/
  - https://typing.python.org/en/latest/spec/generics.html#paramspec
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing decorators with functools.wraps

**Goal:** decorators that keep the wrapped function's name, docs and type signature, and handle sync and async callables.

## 1. Basic shape
```python
import functools, time, logging
from typing import Callable, ParamSpec, TypeVar
P = ParamSpec("P"); R = TypeVar("R")

def timed(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            logging.info("%s took %.3fs", func.__qualname__, time.perf_counter() - start)
    return wrapper
```
`wraps` copies `__module__`, `__name__`, `__qualname__`, `__doc__` (plus `__type_params__` and, on 3.14, `__annotate__`), updates `__dict__` and sets `__wrapped__` (used by `inspect.signature`, pytest, and `unwrap`). Without it, logs, docs and Flask/Click routing break.

## 2. Decorator with arguments (three levels)
```python
def retry(times: int = 3, exceptions: tuple[type[BaseException], ...] = (Exception,)):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
            raise AssertionError("unreachable")
        return wrapper
    return decorator

@retry(times=5, exceptions=(TimeoutError,))
def fetch(): ...
```
Optional-argument form (`@retry` and `@retry(times=5)`): accept `func=None` as first positional and return `decorator` when it is None.

## 3. Async-aware
```python
import inspect
def timed_any(func):
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def awrapper(*a, **kw):
            start = time.perf_counter()
            try: return await func(*a, **kw)
            finally: log(func, start)
        return awrapper
    ...  # sync wrapper as above
```
A sync wrapper around a coroutine function times only coroutine creation, not the work.

## 4. Adding parameters: Concatenate
```python
from typing import Concatenate
def with_db(func: Callable[Concatenate[Connection, P], R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        with pool.connection() as conn:
            return func(conn, *args, **kwargs)
    return wrapper
```

## Gotchas
- Decorator order: the one nearest the `def` applies first. `@classmethod` and `@property` must be outermost (a wrapper over a classmethod raised `TypeError: 'classmethod' object is not callable`; over a property it returned a bound method instead of the value); `@staticmethod` over or under works on 3.10+.
- Decorating methods: `wrapper` receives `self` in `args`; caching decorators (`lru_cache`) on methods keep `self` alive. Use `cached_property` or a per-instance cache.
- Side effects at decoration time run on import; keep registration decorators idempotent.
- `functools.cache`/`lru_cache` require hashable args.

## Verify
- `fetch.__name__ == "fetch"`, `inspect.signature(fetch)` matches the original, and mypy/pyright reveal the same parameter types for the decorated function.

## Checked
- Python 3.14.0 and mypy 2.4.0: `timed`, `retry(times=5, exceptions=...)`, `timed_any` and `with_db` (Concatenate) ran; `wraps` kept `__name__`, `__doc__`, signature and `__wrapped__` (`WRAPPER_ASSIGNMENTS` lists `__annotate__` and `__type_params__` on 3.14); without `wraps` the name became `w` and the doc None; a sync wrapper around a coroutine function timed 0.0000 s while the async wrapper timed 0.20 s; `mypy` revealed `def (x: int) -> int` for the Concatenate-decorated function; decorator-order results as written above. The optional-argument `func=None` form was not run.
