---
id: computing-software.software-engineering.crystal.enum-flags
name: enum-flags
category: computing-software
field: software-engineering
product: crystal
tags: [enum-flags, enums, flags, bitmask, annotation-flags, bit-flags, includes, crystal]
level: practitioner
status: docs-checked
description: "Model permission sets in Crystal with @[Flags] enums: powers of two, None and All, predicates and to_s."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/enum.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flags enums with @[Flags]

Goal: model permission sets.

```crystal
@[Flags]
enum IOMode
  Read   # 1
  Write  # 2
  Async  # 4
end
mode = IOMode::Read | IOMode::Async
mode.read?    # true
mode.write?   # false
IOMode::None.value  # 0
IOMode::All.value   # 7
puts(IOMode::Write | IOMode::Async)  # "Write, Async"
```
- `@[Flags]` makes the first constant `1` and each next one doubles.
- `None` (0) and `All` (the OR of all constants) are added automatically.
- On a flags enum the predicate (`read?`) invokes `includes?` instead of `==`.
- `to_s` separates the set members with a comma and a space.

Verify: spec the printed form of a combination.

## Checked
Checked 2026-11-02 against the crystal-book Enums page. Real error fixed: the skill showed `to_s` as `"Read | Write"`; the page prints `Write, Async`. Removed: `parse`, `&`, `^`, `~`, the non-power-of-two rejection, the unsigned-base-type advice and the "None is not nil" remark.

Method: documentation only; no commands were run.
