---
id: computing-software.software-engineering.crystal.double-splat-named-tuple
name: double-splat-named-tuple
category: computing-software
field: software-engineering
product: crystal
tags: [double-splat-named-tuple, splats-named-args, double-splat, named-tuple, kwargs, options, keyword-arguments, crystal]
level: practitioner
status: draft
description: "Accept arbitrary named arguments with **opts as a NamedTuple and pass hashes or named tuples through to other calls."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Double splat and NamedTuple arguments

Goal: accept options hashes.

- `def configure(**opts)`: `opts` is a `NamedTuple`, e.g. `{host: "x", port: 80}`.
- Forward: `other(**opts)`; build calls from `NamedTuple` literal: `other(**{a: 1})`.
- Mix: `def f(a, *rest, key : Int32 = 0, **others)`.
- Convert for runtime merging: `opts.to_h` (NamedTuple to Hash(Symbol, V)), `opts.merge(extra: 1)`.
- NamedTuple key access `opts[:host]` is checked at compile time; `opts[:missing]?` for optional keys.

Gotchas:
- Keys are compile-time symbols; for dynamic keys use a Hash.
- String keys need `{"my-key": 1}` syntax in NamedTuple literal.
- Splatting a Hash into a call is not supported.

Verify: call with different keysets and observe separate instantiations.
