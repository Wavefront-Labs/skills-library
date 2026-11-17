---
id: computing-software.software-engineering.software-architecture.prototype-pattern
name: prototype-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, creational-patterns, prototype-pattern, gof, cloning, deep-copy, shallow-copy, copy-constructor, templates]
level: practitioner
status: verified
description: "Use the GoF Prototype pattern to create objects by cloning configured instances, handling deep vs shallow copy correctly in each language."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Prototype", "https://refactoring.guru/design-patterns/prototype", "https://docs.python.org/3/library/copy.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototype

**Intent (GoF):** specify the kinds of objects to create using a prototypical instance,
and create new objects by copying this prototype.

## When it fits
- Creating an object is expensive (parsed templates, configured pipelines, loaded
  meshes) and you need many similar ones.
- The set of "kinds" is data-driven at runtime: a palette of preconfigured shapes,
  document templates, game unit archetypes. Register prototypes instead of writing a
  subclass or factory per kind.
- You must copy an object whose concrete type you don't know (polymorphic copy).

## Shape
```python
import copy

class Shape:
    def clone(self) -> "Shape":
        return copy.deepcopy(self)

registry: dict[str, Shape] = {
    "big-red-circle": Circle(r=50, fill="red"),
    "thin-line":      Line(width=1),
}
new_shape = registry["big-red-circle"].clone()
new_shape.move_to(10, 20)
```
C++: virtual `std::unique_ptr<Shape> clone() const` overridden in each subclass
(covariant via helper). Java: copy constructors or a `copy()` method; avoid
`Cloneable`/`Object.clone()` (Bloch's Effective Java discusses its broken contract; confirm the item number in your edition). Kotlin data
classes `copy()` and C# records `with` copy member-wise (Microsoft docs: a reference-type member is copied as a reference, so copy and original share it); JS `structuredClone(obj)` is a deep copy (run: pushing to the clone's array left the original untouched).

## Deep vs shallow is the whole job
- Shallow copy shares nested mutable objects: changing the clone's list changes the
  prototype's. Decide per field: immutable values can be shared; mutable state must be
  copied; identity-bearing references (parent pointers, DB ids, event subscriptions)
  usually must be reset, not copied.
- `copy.deepcopy` handles cycles via a memo, but copies everything reachable,
  including things you meant to share (caches, connections). Implement `__deepcopy__`
  to control it.

## Consequences
+ Add/remove kinds at runtime; fewer subclasses.
- Every class must implement correct cloning; hard with circular references or
  non-copyable resources (file handles, locks).

## Verify
- [ ] Test: mutate every mutable field of a clone; prototype unchanged.
- [ ] Clones get fresh identities (ids, subscriptions) where required.
