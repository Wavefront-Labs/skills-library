---
id: computing-software.software-engineering.software-architecture.flyweight-pattern
name: flyweight-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, flyweight-pattern, gof, memory-optimization, interning, intrinsic-state, extrinsic-state, object-sharing]
level: advanced
status: verified
description: "Use the GoF Flyweight to cut memory when millions of objects share state: split intrinsic vs extrinsic state, intern shared parts, keep flyweights immutable."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Flyweight", "https://refactoring.guru/design-patterns/flyweight", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Integer.html#valueOf(int)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flyweight

**Intent (GoF):** use sharing to support large numbers of fine-grained objects efficiently.

## When it fits (all should be true)
- Very many objects (hundreds of thousands+) and memory is a measured problem.
- Most of each object's state can be shared (intrinsic); the rest can be supplied by
  the context (extrinsic).
- Object identity doesn't matter to the application.
Examples: glyphs in a text editor (font/glyph shared; position extrinsic), map tiles and
particle types in games, tree species in a forest renderer, repeated strings in parsed
logs, cell styles in spreadsheets.

## Shape
```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class TreeType:                 # intrinsic: shared, immutable
    species: str
    texture: bytes
    color: tuple[int, int, int]

_types: dict[tuple, TreeType] = {}
def tree_type(species, texture, color) -> TreeType:
    key = (species, color)
    if key not in _types: _types[key] = TreeType(species, texture, color)
    return _types[key]

@dataclass(slots=True)
class Tree:                     # extrinsic per instance: small
    x: float; y: float
    kind: TreeType
```
A million trees now store two floats and a reference each, not a texture each (run: 10,000 trees with a 10 KB texture took about 0.9 MB shared vs about 102 MB unshared under tracemalloc; needs Python 3.10+ for `slots=True`).

## Rules
- Flyweights must be IMMUTABLE; a shared object mutated by one user changes everyone.
- The factory/cache must be thread-safe if used concurrently, and bounded or weak if
  the key space is large (WeakValueDictionary, Caffeine weakValues).
- Measure before and after (heap histogram, tracemalloc); the pattern adds complexity.

## Built-in flyweights you already use
`Integer.valueOf` cache (-128..127), string interning (`sys.intern`, `String.intern`,
.NET `string.Intern`), enum instances, Java/C# small-value caches. Gotcha: interning
can explain why `==` "works" for small Integers and fails for large ones.

## Data-oriented alternative
Struct-of-arrays plus index-based references (type id into a table) often beats object
flyweights for games and numerical code.

## Verify
- [ ] Heap measurement shows the expected reduction.
- [ ] Shared objects are immutable (frozen dataclass / final fields / readonly).
