---
id: computing-software.software-engineering.python.generators-and-iterators
name: generators-and-iterators
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, python-generators, python-iterators, yield-from, itertools, lazy-evaluation]
level: practitioner
status: verified
description: "Write iterators and generators for streaming data: the iterator protocol, yield from, generator cleanup, itertools pipelines and the single-pass exhaustion trap."
sources:
  - https://docs.python.org/3/reference/datamodel.html#iterator-types
  - https://docs.python.org/3/howto/functional.html
  - https://docs.python.org/3/library/itertools.html
  - https://peps.python.org/pep-0380/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generators and iterators

**Goal:** process large or infinite data in constant memory with readable pipelines.

## 1. Protocol
- Iterable: `__iter__()` returns an iterator. Lists, dicts, files, ranges.
- Iterator: `__next__()` returns the next item or raises `StopIteration`; `__iter__()` returns itself.
- Containers should return a **new** iterator per `__iter__`; iterators are single-pass.

## 2. Generator functions
```python
def read_records(path):
    with open(path, encoding="utf-8") as f:     # closes when generator finishes or is closed
        for line in f:
            if line.strip():
                yield json.loads(line)

def batched_ids(records, n=500):
    batch = []
    for r in records:
        batch.append(r["id"])
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch
```
3.12+: `itertools.batched(iterable, n)` replaces the helper (yields tuples).

## 3. Pipelines
```python
from itertools import islice, chain, groupby, takewhile, tee
recs = read_records("events.jsonl")
errors = (r for r in recs if r["level"] == "error")       # generator expression, lazy
first_100 = list(islice(errors, 100))
total = sum(r["bytes"] for r in read_records("events.jsonl"))
```
`groupby` only groups consecutive equal keys: sort by the key first.

## 4. yield from and delegation
```python
def walk(node):
    yield node
    for child in node.children:
        yield from walk(child)
```
`yield from` forwards `send()`/`throw()` and returns the subgenerator's return value.

## 5. Cleanup
Generators run `finally`/`with` blocks when exhausted, when `.close()` is called, or when garbage collected. Breaking out of a `for` loop leaves the generator suspended until collection (in CPython that is immediate when the last reference drops, but not if you hold the generator in a variable); for deterministic cleanup:
```python
from contextlib import closing
with closing(read_records(p)) as recs:
    for r in recs:
        if done(r): break
```

## Gotchas
- Exhaustion: iterating a generator twice yields nothing the second time, silently. Materialise with `list()` or make the source re-iterable (a class with `__iter__`).
- `if gen:` is always true; check emptiness with `next(gen, sentinel)`.
- `tee` buffers everything one branch is ahead of the other; it can use as much memory as a list.
- A `StopIteration` raised inside a generator becomes `RuntimeError` (PEP 479); return instead.
- Lazy evaluation defers exceptions and late-binds variables: generator expressions capture loop variables at consumption time except for the first `for` iterable.

## Verify
- Memory stays flat (`tracemalloc` peak) when piping a multi-GB file through the generator, and a unit test asserts the pipeline result on a small fixture.

## Checked
- Python 3.14.0: `itertools.batched` yields tuples; a spent generator yields nothing and `bool(gen)` is True; `for ... break` closed a temporary generator at once while a held one closed on `del`; `StopIteration` inside a generator gave `RuntimeError: generator raised StopIteration`; late binding: inner `for` iterables and free variables are read at consumption, the first iterable at creation; `tee` of 1e6 ints held about 41 MB when one branch ran ahead; `yield from` forwarded `send` and the return value; `groupby` groups consecutive keys only.
