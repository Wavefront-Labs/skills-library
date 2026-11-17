---
id: computing-software.software-engineering.go.iota-and-typed-untyped-constants
name: iota-and-typed-untyped-constants
category: computing-software
field: software-engineering
product: go
tags: [go, go-types-values, go-iota-constants, constants, iota]
level: practitioner
status: docs-checked
description: "Define enum-like constants with iota, skip values, and understand untyped constant arithmetic and default types."
sources:
  - https://go.dev/ref/spec#Constants
  - https://go.dev/ref/spec#Iota
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# iota and typed/untyped constants

**Goal:** model enums and bit flags with `iota` and avoid surprises from untyped constant rules.

```go
type Level uint8

const (
    Debug Level = iota // 0
    Info               // 1
    _                  // 2 skipped on purpose
    Error              // 3
)

type Perm uint8
const (
    Read Perm = 1 << iota // 1
    Write                 // 2
    Exec                  // 4
)
```

Per the spec, inside a constant declaration `iota` is the index of the ConstSpec, starting at zero, as an untyped integer constant; each `const (...)` block restarts at 0 (a lone `const x = iota` is 0). Several uses of `iota` in one ConstSpec share the same value. A ConstSpec with an omitted expression list repeats the last non-empty expression list, re-evaluated with the new `iota`, which is what the examples above rely on.

Untyped constants have arbitrary precision at compile time and a default type when a typed value is needed: `bool`, `rune`, `int`, `float64`, `complex128` or `string` by kind. A constant is converted to the type of the other operand when mixed with a typed value. Untyped constants such as `const Big = 1 << 62` can be assigned wherever the value is representable: `var f float32 = Big` is fine (rounding is allowed), `var i int32 = Big` is a compile error because the value does not fit.

## Gotchas
- Never persist or transmit raw `iota` values if you may reorder the list; insert new members at the end or assign explicit numbers.
- Untyped constant expressions are evaluated exactly: `5 / 2` is integer division (2), while `5 / 2.0` is 2.5. If untyped operands of a binary operation (not a shift) have different kinds, the result takes the later kind in this order: integer, rune, floating-point, complex.

## Verify
A table test that asserts `Read|Write == 3` and that the skipped member leaves the expected value (`Error == 3`).

## Checked
Checked 2026-11-08 against the Go specification (Constants, Iota, Constant expressions, Operators) on the single-page spec.
Removed as not in the spec: the `stringer` and `go vet` advice, and the claim that any integer value converts to the enum type.
Method: documentation only; no commands were run.
