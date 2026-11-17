---
id: computing-software.software-engineering.crystal.overload-ordering
name: overload-ordering
category: computing-software
field: software-engineering
product: crystal
tags: [overload-ordering, overloading, overload-resolution, specificity, restriction-order, no-overload-matches, ambiguity, crystal]
level: advanced
status: draft
description: "Understand how the compiler orders overloads: more specific restriction first, then definition order, and how to debug."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overload resolution order and specificity

Goal: predict which overload is chosen.

- Methods with more specific type restrictions are tried before general ones; an unrestricted parameter matches last.
- Among equals, a later-defined method is tried first (so reopen classes carefully).
- Subclass overloads take priority over inherited ones; `super` reaches the parent.
- Error `no overload matches 'foo' with type X` lists every candidate and which arg mismatched; use that to find the gap.
- With unions, the compiler dispatches each member separately, so every member must find a match.

Gotchas:
- Adding a generic fallback can silently capture calls formerly erroring.
- Positional vs named matching differs: named args can reorder.
- Literals adapt (`1` fits Int8 if the restriction says so).

Verify: temporarily call with an unsupported type and read the candidate list.
