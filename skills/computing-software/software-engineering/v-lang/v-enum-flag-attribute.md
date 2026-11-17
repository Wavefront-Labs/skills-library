---
id: computing-software.software-engineering.v-lang.v-enum-flag-attribute
name: v-enum-flag-attribute
category: computing-software
field: software-engineering
product: v-lang
tags: [v-enum-flag-attribute, enums, flag enum, flag, bit flags, bitmask, has, set, clear, toggle, v-lang]
level: practitioner
status: docs-checked
description: "Create bit-flag enums with @[flag] and use has, set, clear and toggle methods plus bitwise combination."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flag enums with @[flag]

Goal: pack boolean options into one integer.

```v
@[flag]
enum Perm { read write exec }

mut p := Perm.read
p.set(.write | .exec)
p.has(.read | .exec)  // true: at least one of the flags is set
p.all(.read | .write) // true: all of the flags are set
p.toggle(.exec)
p.clear(.read)
```
- `@[flag]` makes an enum usable as a bitfield: `read` is 1, `write` is 2, `other` is 4 in the docs example, and `int(full) == 7` after `set_all()`.
- Generated helpers shown in the docs: `has` (at least one flag set), `all` (all set), `set`, `clear`, `toggle`, `set_all`, `clear_all`, `is_empty`, and the static `Perm.zero()` for the empty set.
- Combine flags with `|` (`Perm.read | .write`); compare with `==`.
- `Perm.from('read')!` and `Perm.from(2)!` build a flag value from a name or integer; `Perm.from('')!` is the empty set.
- Mutators need a mutable receiver in safe code; an `unsafe` block can mutate through an immutable binding. Named constants are invalid receivers.
- Flag enum initializers specify bit positions and must be known at compile time.
- `@[_allow_multiple_values]` is a separate attribute that allows duplicate values in an ordinary enum.

Verify: `assert (Perm.read | Perm.write).has(.write)` (adapt from the docs example in an assert-based test).

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Attributes" and "Enums"): the `@[flag]` example and every helper listed, mutable receiver rule, bit-position initializers. Removed as not stated there: the older `[flag]` syntax remark, the 64-flag limit, "test with `&`", the printed form `Perm{...}`, and the claim that explicit values cannot be set (the docs say initializers give bit positions).

Method: documentation only; no commands were run.
