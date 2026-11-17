---
id: computing-software.software-engineering.python.memoisation-with-functools-cache
name: memoisation-with-functools-cache
category: computing-software
field: software-engineering
product: python
tags: [python, lru-cache, functools-cache, cached-property, memoization, ttl-cache, python-performance]
level: practitioner
status: verified
description: "Cache expensive pure function results with functools.cache/lru_cache and cached_property: hashable args, maxsize, method caching leaks, invalidation, TTL and thread safety."
sources: ["https://docs.python.org/3/library/functools.html#functools.lru_cache", "https://docs.python.org/3/library/functools.html#functools.cached_property", "https://docs.python.org/3/faq/programming.html#how-do-i-cache-method-calls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memoisation with functools.cache

**Goal:** skip repeated expensive work with a one-line decorator, without memory leaks
or stale data.

## Basics
```python
from functools import cache, lru_cache

@cache                         # unbounded (== lru_cache(maxsize=None)), fastest
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=1024)       # bounded, evicts least recently used
def load_schema(name: str) -> dict: ...

load_schema.cache_info()       # CacheInfo(hits=..., misses=..., maxsize=1024, currsize=...)
load_schema.cache_clear()
```

## Rules
- Arguments must be hashable: lists/dicts raise `TypeError: unhashable type`. Convert to
  tuples/frozensets at the call site or wrap.
- Equal arguments of different types are "usually" one entry unless `typed=True`, but a
  single `int`/`str` argument is a fast-path key: with one argument `f(1)` and `f(1.0)` were two
  entries on 3.14 (two arguments, `f(1, 2)` and `f(1.0, 2)`, shared one). Do not rely on either;
  `f(a=1)` and `f(1)` are different keys.
- Only cache pure functions (output depends only on args). Caching something that reads
  the clock, DB or env returns stale data forever.
- Returned objects are shared: if callers mutate a cached list, everyone sees it. Return
  tuples/frozen dataclasses.

## Methods: the leak
```python
class Repo:
    @lru_cache(maxsize=None)          # BAD: cache holds `self` forever -> instances never freed
    def lookup(self, key): ...
```
Options:
- `functools.cached_property` for per-instance, argument-less values (stored in the
  instance `__dict__`; needs no `__slots__`; delete the attribute to invalidate).
- Per-instance cache in `__init__`: `self.lookup = lru_cache(maxsize=256)(self._lookup)`.
- Module-level function cached on the real key (not on `self`).

## Expiry (TTL)
functools has no TTL. Use `cachetools.TTLCache` with `cachetools.cached(cache, lock=threading.Lock())`,
or include a time bucket in the key: `get_rates(int(time.time() // 300))` for 5-minute freshness.

## Concurrency
`lru_cache` is thread-safe for its internal state, but two threads missing simultaneously
both compute the value (no request coalescing). For async functions, `lru_cache` caches the
coroutine object, which can be awaited only once - use `async-lru` or cache the result manually.

## Verify
- [ ] `cache_info()` shows a meaningful hit rate under realistic load.
- [ ] No `@lru_cache` directly on instance methods of long-lived or numerous objects.

## Checked
- Python 3.14.0: `@cache` fib(50) gave `CacheInfo(hits=48, misses=51, maxsize=None, currsize=51)` and `cache_parameters()` shows maxsize None; `f(a=1)` vs `f(1)` were separate entries; `typed=True` separated 1 and 1.0; list argument raised `unhashable type: 'list'`; an `lru_cache` on a method kept the instance alive after `del` and `gc.collect()`; a cached coroutine function raised "cannot reuse already awaited coroutine" on the second await; four threads missing together computed 4 times; cachetools `TTLCache` with `cached(cache, lock=...)` recomputed after the TTL.
