---
id: computing-software.software-engineering.refactoring.encapsulate-record-and-collection
name: encapsulate-record-and-collection
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, encapsulation, encapsulate-collection, encapsulate-record, unmodifiable-view, defensive-copy, fowler-catalog]
level: practitioner
status: draft
description: "Encapsulate Record and Encapsulate Collection: replace raw dicts/structs with classes and stop callers mutating internal lists via add/remove methods and read-only views."
sources:
  - https://refactoring.com/catalog/encapsulateRecord.html
  - https://refactoring.com/catalog/encapsulateCollection.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encapsulate Record / Encapsulate Collection

## Encapsulate Record
**Smell:** a plain dict/JSON blob/struct (`org["name"]`) passed everywhere; no single place to add validation, derived values, or rename a field.

Mechanics:
1. Encapsulate Variable on the variable holding the record (a getter returning it).
2. Create a class wrapping the record; the getter returns an instance of it.
3. Add accessors for each field; switch callers one at a time, running tests.
4. Once all callers use accessors, make the raw data private; drop "get raw data".
5. For nested records, start with updates (they matter most); reads can return deep copies or read-only proxies for a while.

```python
# before
organization = {"name": "Acme", "country": "GB"}
# after
class Organization:
    def __init__(self, data): self._name, self._country = data["name"], data["country"]
    @property
    def name(self): return self._name
    @name.setter
    def name(self, v): self._name = v
```
For value-like records use an immutable type (`@dataclass(frozen=True)`, Java `record`, C# `record`); then there is nothing to encapsulate on the write side.

## Encapsulate Collection
**Smell:** `person.courses` getter returns the internal list, so any caller can `person.courses.append(c)` and the owner never knows (no validation, no events, broken invariants).

Mechanics:
1. Encapsulate the variable if not already.
2. Add `add_course(c)` and `remove_course(c)` on the owner (with validation and error on removing a missing item).
3. Find every mutation of the collection through the getter and switch it to the new methods.
4. Change the getter to return a read-only view or copy:
   - Java `Collections.unmodifiableList(courses)` or `List.copyOf`
   - C# `IReadOnlyList<T>` / `AsReadOnly()`
   - Python `tuple(self._courses)` or return a `Sequence` type hint
   - JS `[...this.#courses]` or `Object.freeze`
5. Replace the setter that took a whole list with one that copies its input (`self._courses = list(courses)`), or remove it.

## Gotchas
- A read-only view still reflects later internal changes; a copy does not. Pick deliberately and document it.
- Returning copies of big collections in hot loops costs allocations; return an iterator or view instead.
- ORMs (JPA, EF Core) map the backing field; configure field access so the encapsulated collection still persists.

## Verify
- [ ] Grep shows no `.courses.append/add/push/remove` outside the owner.
- [ ] A test asserts mutating the returned collection raises or has no effect on the owner.
