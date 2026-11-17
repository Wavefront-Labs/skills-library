---
id: computing-software.software-engineering.crystal.enum-basics
name: enum-basics
category: computing-software
field: software-engineering
product: crystal
tags: [enum-basics, enums, enum, enum-members, enum-parse, enum-predicate, base-type, case-enum, crystal]
level: intro
status: docs-checked
description: "Define Crystal enums: values, underlying type, predicates, methods, integer conversion and symbol autocasting."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/enum.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining and using enums

Goal: define typed constants.

```crystal
enum Color : UInt8
  Red
  Green
  Blue = 5
  Yellow            # 6
  def warm?; red?; end
end
Color::Green.value   # 1, a UInt8
Color.new(1)         # Green
Color.new(10)        # allowed; prints "10"
```
- Values start at `0` and increment by one; any member can be overwritten and the next follows it. The value type is `Int32` unless given (`: UInt8`); only integer types are allowed.
- Each member has the enum's type; `value` returns the underlying integer. All enums inherit from `Enum`.
- Predicate methods are generated per member from `String#underscore` (`red?`).
- `Color.new(int)` converts an integer, mainly meant for C values; non-member integers are allowed and print as the number.
- Enums can have methods and class variables, but not instance variables.
- A parameter restricted to an enum accepts a member or a symbol (`paint :red`), cast at compile time; an unknown symbol is a compile error. This autocast does not apply in `case`; use `in .red?` or `in Color::Red`.

Verify: `puts Color.new(1)` prints `Green`.

## Checked
Checked 2026-11-02 against the crystal-book Enums page. Removed: `parse`, `parse?`, `from_value`, `names`, `values`, `each` (API docs were not read), lowercase-member error, the `to_s` remark.

Method: documentation only; no commands were run.
