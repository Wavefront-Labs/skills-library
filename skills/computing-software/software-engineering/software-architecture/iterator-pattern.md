---
id: computing-software.software-engineering.software-architecture.iterator-pattern
name: iterator-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, iterator-pattern, generators, lazy-evaluation]
level: practitioner
status: verified
description: "Apply the Iterator pattern with language-native iteration (generators, IEnumerable, Iterator traits): lazy traversal, custom collections, resource cleanup and modification safety."
sources: ["https://refactoring.guru/design-patterns/iterator", "https://docs.python.org/3/library/stdtypes.html#iterator-types", "https://learn.microsoft.com/en-us/dotnet/csharp/iterators", "https://doc.rust-lang.org/std/iter/trait.Iterator.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterator

Provide sequential access to elements of an aggregate without exposing its representation. In
modern languages the pattern is built in; the craft is using it well.

## Native forms
| Language | Protocol | Easy implementation |
|---|---|---|
| Python | `__iter__` / `__next__`, `StopIteration` | generator function with `yield` |
| C# | `IEnumerable<T>` / `IEnumerator<T>` | `yield return` |
| Java | `Iterable<T>` / `Iterator<T>` | implement, or expose `Stream<T>` |
| JS/TS | `[Symbol.iterator]()`, async `[Symbol.asyncIterator]` | `function*`, `async function*` |
| Rust | `Iterator` trait `next()` | impl trait; adapters `map/filter` |
| Go | range-over-func (Go 1.23+; `iter` package is absent in 1.22) `iter.Seq[T]` | `func(yield func(T) bool)` |

## Uses
- Custom collections (tree in-order traversal) without exposing nodes.
- **Lazy/streaming** sequences: paginated API results, file lines, DB cursors, infinite sequences.
```python
def all_invoices(client):
    token = None
    while True:
        page = client.list_invoices(page_token=token)
        yield from page.items
        token = page.next_page_token
        if not token: return
```
- Multiple traversal strategies over one structure (depth-first vs breadth-first iterators).

## Gotchas
- **Modification during iteration**: Java throws `ConcurrentModificationException`; Python dicts raise
  `RuntimeError`; C# throws `InvalidOperationException`. Iterate over a copy or collect changes first.
- **Single-use**: generators/iterators are exhausted after one pass; return an iterable (re-iterable)
  from APIs when callers may loop twice.
- **Resource cleanup**: iterators over files/cursors must close if abandoned early: Python
  generators get `GeneratorExit` (use `with` inside), C# `IDisposable` enumerators via `foreach`,
  Go iterator funcs must respect `yield` returning false.
- Lazy evaluation defers exceptions and side effects until iteration; surprising when debugging.
