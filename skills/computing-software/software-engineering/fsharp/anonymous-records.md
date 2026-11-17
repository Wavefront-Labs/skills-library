---
id: computing-software.software-engineering.fsharp.anonymous-records
name: anonymous-records
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, anonymous-records, fsharp-tuples-records, anon-records, struct-anonymous-records]
level: practitioner
status: docs-checked
description: "Use anonymous records for lightweight shaped data, struct anonymous records, and know their type-compatibility rules."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anonymous records
**Goal:** return shaped data without declaring a type.

```fsharp
let r = {| Name = "Ada"; Age = 36 |}
let r2 = {| r with Age = 37 |}
let sr = struct {| X = 1; Y = 2 |}              // struct anonymous record
let describe (p: {| Name: string; Age: int |}) = p.Name
```
- Anonymous records are reference types by default; use `struct` for a struct anonymous record.
- `{| data with Y = 3 |}` copies an existing record; it can also add or change fields and produce a different shape.
- They use structural equality and comparison, like record types (when all constituent types support it).
- They interoperate with .NET APIs that require C# anonymous types.

## Gotchas
- It is not currently possible to define an anonymous record with mutable data.

## Self-check
`{| A = 1 |} = {| A = 1 |}` is true.
## Checked
2026-11-02. Confirmed against Microsoft Learn "Anonymous Records" (F# language reference): syntax, struct, copy-and-update, structural equality, C# interop, no mutable data. Removed: alphabetical field ordering, the "avoid in public APIs" and JSON advice (the page says they are serializable).
Method: documentation only; no commands were run.
