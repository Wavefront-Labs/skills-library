---
id: computing-software.software-engineering.ada.generic-packages-subprograms
name: generic-packages-subprograms
category: computing-software
field: software-engineering
product: ada
tags: [ada, generic-packages-subprograms, ada-generics]
level: practitioner
status: docs-checked
description: "Write an Ada generic with formal type, object and subprogram parameters and instantiate it with new."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/advanced-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic packages and subprograms
```ada
generic
   type Item is private;
   with function "<" (L, R : Item) return Boolean is <>;
procedure Sort (A : in out Item_Array);
procedure Int_Sort is new Sort (Item => Integer);   -- "<" picked by <>
```
- Formal type kinds: `private` (any definite type), `limited private`, `(<>)` discrete, `range <>` (integer types), `digits <>` (floating point).
- A generic body repeats the declaration without the `generic` keyword.
- Formal subprograms use `with function ... is <>` to pick a matching visible operation by default.
## Gotchas
- Formal objects behave like subprogram parameters.
## Self-check
Instantiate Sort for Integer and Float and confirm both sort.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Generics: formal `private`, `(<>)`, `digits <>`, `range <>`, `limited private`, `with function ... is <>`, generic body syntax, formal objects. Removed `array`/`access` formal kinds, the instantiation-timing claim and the `-gnatn` advice (not on the pages read). The `Sort` example is illustrative.
Method: documentation only; no commands were run.
