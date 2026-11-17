---
id: computing-software.software-engineering.fsharp.enums-flags
name: enums-flags
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, enums-flags, fsharp-unions, enumerations, flags-enum]
level: practitioner
status: docs-checked
description: "Declare F# enums, convert with enum and int, and combine flags, noting that enum matches are never exhaustive."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/enumerations
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Enums
**Goal:** model .NET-style integer enums.

```fsharp
type Color =
    | Red = 0
    | Green = 1
    | Blue = 2

[<System.Flags>]
type Perm =
    | None = 0
    | Read = 1
    | Write = 2
    | Exec = 4

let c = Color.Red
let n = int c
match c with
| Color.Red -> "r"
| Color.Green -> "g"
| _ -> "other"      // needed: enums can hold values outside the known cases
```
- Enum values are explicit integers; use `Type.Case` to refer to them, since cases are always qualified.
- Mark bit-position enums with `[<Flags>]`.
- Warning FS0104 (`Enums may take values outside known cases.`) arises because enums can be assigned arbitrary underlying values; `#nowarn "104"` makes exhaustive matching consider only the declared cases.

## Gotchas
- An enum can hold values outside its declared cases (directly or through bitwise operations), so keep the `_` rule above.

## Self-check
`int Color.Blue` is 2.

## Checked
2026-11-02. Confirmed against Learn "Enumerations": explicit integer values, Type.Case qualification, [<Flags>] for bit positions, FS0104 and #nowarn "104", and cases emitted as public. Removed: the prefer-a-union advice, validate-outside-values advice, Enum.IsDefined, the enum<...> cast and bitwise-operation examples, the ToString self-check and the power-of-two rule (not on the page).
Method: documentation only; no commands were run.
