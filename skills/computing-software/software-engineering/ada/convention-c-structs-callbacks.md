---
id: computing-software.software-engineering.ada.convention-c-structs-callbacks
name: convention-c-structs-callbacks
category: computing-software
field: software-engineering
product: ada
tags: [ada, convention-c-structs-callbacks]
level: advanced
status: docs-checked
description: "Match C layouts in Ada with Convention C records and enums, and generate bindings with gcc -fdump-ada-spec."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/Ada_For_The_Embedded_C_Developer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C structs, enums, arrays and callbacks
```ada
type Pt is record X, Y : int; end record with Convention => C;
```
- Generate bindings: `gcc -c -fdump-ada-spec -C header.h`; `-fada-spec-parent=Name` sets the parent unit for the generated bindings.
- C enums: `type E is (A, B) with Convention => C;`.
## Gotchas
- The generator ignores a `struct` declaration it cannot map and replaces references to it with `System.Address`.
## Self-check
Generate bindings for a small header and compare them with the header.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Interfacing with C: `Convention => C` on records and enums, `-fdump-ada-spec -C`, `-fada-spec-parent`, struct-to-`System.Address` behaviour. Removed access-to-subprogram callbacks, `Interfaces.C.Pointers`, enum `Size` and the pass-by-pointer self-check (not on the pages read).
Method: documentation only; no commands were run.
