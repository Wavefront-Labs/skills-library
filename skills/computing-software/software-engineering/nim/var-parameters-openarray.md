---
id: computing-software.software-engineering.nim.var-parameters-openarray
name: var-parameters-openarray
category: computing-software
field: software-engineering
product: nim
tags: [var-parameters-openarray, procedures-basics, var-parameter, openarray, by-reference, mutation, lent, copy, nim]
level: practitioner
status: docs-checked
description: "Pass by mutable reference with Nim var parameters, accept arrays and seqs with openArray, and know the limits."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# var parameters and openArray

Goal: control copying and mutation at call boundaries.

- Parameters are immutable in the proc body, which lets the compiler pass them in the most efficient way. Var parameters are never necessary for efficient passing, because the compiler is free to pass non-var arguments by reference.
- `proc divmod(a, b: int; res, remainder: var int)` modifies the caller's variables. The argument for a var parameter has to be an l-value, and var parameters are implemented as hidden pointers.
- For two return values the manual suggests returning a tuple instead, `tuple[res, remainder: int]`, with unpacking `var (x, y) = divmod(8, 5)`.
- `openArray[T]` accepts any array (any index type) or seq with a compatible base type. It can only be used for parameters, is indexed by int from 0, and supports `len`, `low` and `high`. Open arrays cannot be nested, so multidimensional open arrays are not supported.
- `varargs[T]` is like an `openArray` parameter, and the compiler converts the argument list to an array only when it is the last parameter.
- The manual's own example takes `var openArray[T]` (for in-place modification of elements).

Verify: a proc taking `var int` parameters changes the caller's variables.

## Checked

2026-11-08. Read the Nim tutorial sections Parameters, Open arrays and Varargs and the manual Var parameters section.

Removed as unconfirmed: `toOpenArray`, `lent T`, the claims about hidden-reference passing of large parameters beyond the note above, and the growth/shrink comparison between var seq and openArray. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
