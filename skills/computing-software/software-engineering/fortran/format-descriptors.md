---
id: computing-software.software-engineering.fortran.format-descriptors
name: format-descriptors
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, format-descriptors, fortran-io-formatted]
level: practitioner
status: draft
description: "Format output with edit descriptors I, F, E, ES, G, A, X, and repeat counts and slashes."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Format edit descriptors
**Goal:** produce predictable text output.
```fortran
write (*, '(a, i5, f10.3, es12.4)') 'n=', 42, 3.14159, 6.022e23
write (*, '(3(f8.2, 1x))') a(1:3)
write (*, '(i0)') n              ! minimal width
```
- `Iw`, `Fw.d`, `Ew.d`, `ESw.d` (scientific), `Aw`, `Lw`, `Xn` spaces, `/` newline, `Tn` tab, `nP` scale.
- `I0`, `F0.d` (F2008) produce minimal width; `g0` (F2008) general minimal.
- Format string can be a variable or a `format` statement with a label.
- Reusing a format: format reversion restarts at the last open group when the list has more items.
## Gotchas
- A field too narrow prints asterisks.
- `E` prints `0.xxxE+yy` form; use `ES` for `x.xxxE+yy`.
## Self-check
Print `1234.5678` with `f8.2`; expect ` 1234.57`.
