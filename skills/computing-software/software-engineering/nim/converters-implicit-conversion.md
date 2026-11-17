---
id: computing-software.software-engineering.nim.converters-implicit-conversion
name: converters-implicit-conversion
category: computing-software
field: software-engineering
product: nim
tags: [converters-implicit-conversion, funcs-iterators-converters, converter, implicit-conversion, type-conversion, nim]
level: advanced
status: docs-checked
description: "Define Nim converters for implicit type conversion, and weigh their risks against explicit conversion procs."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converters and implicit conversions

Goal: add implicit conversions sparingly.

- A `converter` is like an ordinary proc except that it enhances the "implicitly convertible" type relation: `converter toBool(x: int): bool = x != 0` lets `if 4:` compile. The manual labels that example "bad style ahead".
- A converter can also be called explicitly for readability.
- Implicit converter chaining is not supported: with converters A to B and B to C, the conversion from A to C is not provided.
- The manual says ordinary procs are often preferred over type conversions in Nim, for example `$` as the toString operator and `toFloat` / `toInt` between floats and integers.

Verify: passing the source type to a proc declared for the target type compiles only when the converter is in scope.

## Checked

2026-11-08. Read the Nim manual Converters section and the type-conversion paragraph that recommends ordinary procs.

Removed as unconfirmed on the manual: that converters apply only after exact and generic matches fail, the safe-use list (string wrapper, distinct, cstring), the claim that converters export with the module, and the notes on cryptic overload errors. Dropped the tutorial and lib index sources (not used).

Method: documentation only; no commands were run.
