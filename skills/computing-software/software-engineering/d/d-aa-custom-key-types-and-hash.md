---
id: computing-software.software-engineering.d.d-aa-custom-key-types-and-hash
name: d-aa-custom-key-types-and-hash
category: computing-software
field: software-engineering
product: d
tags: [d-aa-custom-key-types-and-hash, associative-arrays, tohash, opequals, hashof, aa-key, custom-key, struct-key, d]
level: advanced
status: docs-checked
description: "Use structs and classes as AA keys by defining toHash and opEquals consistently, with const/nothrow/@safe signatures and hashOf for combining fields."
sources:
  - https://dlang.org/spec/hash-map.html
  - https://dlang.org/spec/class.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom key types, toHash and opEquals

Goal: make a user type a valid AA key.

```d
struct P {
    int x, y;
    size_t toHash() const @safe pure nothrow { return hashOf(y, hashOf(x)); }
    bool opEquals(const P o) const { return x == o.x && y == o.y; }
}
int[P] grid;
```
- Rule: values that compare equal must hash equal.
- A struct or union key gets a default hash and comparison from its fields; define `toHash`/`opEquals` only for custom semantics (case-insensitive, floats).
- For classes override `override size_t toHash() @trusted nothrow` and `override bool opEquals(Object o)`.
- `hashOf(value, seed)` chains hashing.
- Do not mutate a key after insertion (undefined behaviour per the spec).

Gotchas:
- The compiler cannot always detect mismatched `opEquals`/`opCmp` signatures; a key type that overrides `opCmp` but not `opEquals` may be rejected.
- Hashing floats with NaN breaks equality.

Verify: insert two equal keys and assert `grid.length == 1`.

## Checked

Date 2026-11-02. Confirmed default struct hash/equality, toHash/opEquals/opCmp requirements and no key mutation (Associative Arrays spec). Fixed the class toHash signature (@trusted nothrow, no const) and removed the immutable-key advice.

Method: documentation only; no commands were run.
