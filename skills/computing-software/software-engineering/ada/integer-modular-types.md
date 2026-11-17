---
id: computing-software.software-engineering.ada.integer-modular-types
name: integer-modular-types
category: computing-software
field: software-engineering
product: ada
tags: [ada, integer-modular-types, ada-scalar-types]
level: practitioner
status: draft
description: "Declare Ada signed (range) and modular (mod) integer types, wraparound behaviour, Integer'First/Last and overflow checks."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/chapters/strongly_typed_language.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Integer and modular types
```ada
type Percent is range 0 .. 100;
type Byte    is mod 2**8;          -- wraps: 255 + 1 = 0
type Count   is new Integer range 0 .. Integer'Last;
```
- Distinct types do not mix: `Percent` + `Integer` needs `Integer (P)`.
- Signed overflow raises `Constraint_Error` (checks on by default); modular wraps silently.
- Attributes: `T'First`, `T'Last`, `T'Size`, `T'Pos`, `T'Succ`.
## Gotchas
- `-gnatp` or `pragma Suppress` removes range checks; do not release with it unless proven safe (e.g. by SPARK).
## Self-check
Add 1 to `Byte'Last` (wraps to 0) and to `Percent'Last` (raises Constraint_Error).
