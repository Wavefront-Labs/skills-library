---
id: computing-software.software-engineering.fsharp.records
name: records
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, records, fsharp-tuples-records, record-copy-update, record-types]
level: intro
status: docs-checked
description: "Define F# records, create copies with the with keyword and rely on structural equality, plus struct and mutable record fields."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/records
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/copy-and-update-record-expressions
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Records
**Goal:** model immutable data with named fields.

```fsharp
type Person = { Name: string; Age: int }
let p = { Name = "Ada"; Age = 36 }
let older = { p with Age = p.Age + 1 }     // copy-and-update
let same = p = { Name = "Ada"; Age = 36 } // true: structural equality

[<Struct>]
type Point = { X: float; Y: float }

type Account = { Id: int; mutable Balance: decimal }
```
- Records are reference types by default; `[<Struct>]` makes a struct record.
- Records are immutable by default; `mutable` opts a field in.
- Type inference uses the labels, but avoid the short form when another record type has the same labels.
- Records have structural equality; `[<ReferenceEquality>]` switches to reference equality.
- Records take members (`static member`, instance members); they have no fields in the member list.
- Pattern: `let { Name = n } = p`; `match p with { Age = a } when a > 17 -> ...`.

## Self-check
`{ p with Age = 40 }` leaves `p.Age` unchanged.

## Checked
2026-11-02. Confirmed against Learn "Records": reference type by default, [<Struct>], mutable fields, copy-and-update with `with`, record expressions and label-based inference, structural equality, [<ReferenceEquality>], members on records and pattern matching with records. Removed: the intrinsic `type X with` extension, automatic comparison, hashing and ToString claims, the [<CustomEquality; NoComparison>] advice, the non-comparable-record Map key gotcha, the 'latest declared wins' rule and the field-addition note (not on the pages read).
Method: documentation only; no commands were run.
