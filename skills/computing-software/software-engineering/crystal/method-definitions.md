---
id: computing-software.software-engineering.crystal.method-definitions
name: method-definitions
category: computing-software
field: software-engineering
product: crystal
tags: [method-definitions, types-and-methods, def, class, initialize, property, getter, setter, instance-variables, class-methods, self, crystal]
level: intro
status: draft
description: "Define classes, instance variables, initialize, getter/setter/property macros, class methods and the self receiver."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defining methods, classes and initialize

Goal: write a typical class.

```crystal
class Point
  getter x : Int32
  property y : Int32
  def initialize(@x, @y); end
  def self.origin; new(0, 0); end
  def to_s(io : IO) : Nil
    io << "(" << @x << ", " << @y << ")"
  end
end
```
- `getter`, `setter`, `property` (plus `getter?`, `property!`) generate accessors; `@x` in initialize params assigns directly.
- Override `to_s(io)` and `inspect(io)`, not a string-returning `to_s`, for efficiency.
- Methods return the last expression; `return` is optional.
- Every instance variable must be initialised in all `initialize` paths or be nilable.

Gotchas:
- `getter!` raises on nil; `getter?` creates a `?` predicate.
- Calling `new` with the wrong arity is a compile-time error, not runtime.

Verify: `puts Point.new(1, 2)` prints (1, 2).
