---
id: computing-software.software-engineering.python.custom-iterator-protocol
name: custom-iterator-protocol
category: computing-software
field: software-engineering
product: python
tags: [python, py-iteration, iterator-protocol-custom, iter, next, stopiteration, iterable, reiterable]
level: practitioner
status: docs-checked
description: "Implement __iter__ and __next__ correctly, separate iterables from iterators so objects can be looped repeatedly, and use the two-argument iter() sentinel form."
sources: ["https://docs.python.org/3/library/stdtypes.html#iterator-types", "https://docs.python.org/3/library/functions.html#iter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom iterator protocol

- **Iterable**: has `__iter__()` returning an iterator. Lists, files, your collection classes.
- **Iterator**: has `__next__()` and `__iter__()` returning itself; raises `StopIteration` when exhausted and must keep raising it afterwards.

## Re-iterable collection with a generator `__iter__` (preferred)
```python
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self):                 # each call = a fresh, independent iterator
        n = self.n
        while n > 0:
            yield n
            n -= 1

c = Countdown(3)
assert list(c) == [3, 2, 1] and list(c) == [3, 2, 1]
```

## Hand-written iterator (only when you need state beyond a generator)
```python
class Pages:
    def __init__(self, fetch): self._fetch, self._page, self._buf = fetch, 0, []
    def __iter__(self): return self
    def __next__(self):
        if not self._buf:
            self._buf = self._fetch(self._page); self._page += 1
            if not self._buf: raise StopIteration
        return self._buf.pop(0)
```

## Sentinel form
`iter(callable, sentinel)` calls `callable()` until it returns the sentinel:
`for block in iter(lambda: f.read(8192), b""): ...`

## Gotchas
- If `__iter__` returns `self` on a collection, a second `for` loop sees nothing: the classic "works once" bug.
- Never raise `StopIteration` inside a generator; since 3.7 (PEP 479) it becomes `RuntimeError`.
- `next(it, default)` avoids the exception; `list(it)` exhausts it.
- Modifying a sequence while iterating over it is unsafe (the tutorial advises iterating over a copy or creating a new collection).

## Verify
- [ ] Iterate the object twice and assert equal results.
- [ ] `iter(x) is x` is true for iterators (their `__iter__` returns `self`), false for re-iterable collections.
- [ ] A test calls `next()` past the end twice and expects `StopIteration` both times.

## Checked

- 2026-11-03: checked against the CPython docs `builtins/stdtypes.rst` (iterator protocol: `__iter__` returns the iterator, `__next__`, must keep raising `StopIteration`), `builtins/functions.rst` (`iter(callable, stop_value)`, `next(iterator, default)`), `whatsnew/3.7.rst` (PEP 479: `StopIteration` in generators becomes `RuntimeError`) and `tutorial/controlflow.rst` (iterate over a copy).

Method: documentation only; no commands were run.
