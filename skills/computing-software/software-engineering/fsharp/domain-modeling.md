---
id: computing-software.software-engineering.fsharp.domain-modeling
name: domain-modeling
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, domain-modeling, fsharp-architecture, type-driven-design, functional-core]
level: practitioner
status: draft
description: "Model a domain with records, unions and smart constructors keeping a pure core and effects at the edge."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domain modelling
**Goal:** design with types, not conditionals.

```fsharp
type CustomerId = CustomerId of int
type Quantity = private Quantity of int
module Quantity =
    let create n = if n > 0 then Ok (Quantity n) else Error "must be positive"
    let value (Quantity n) = n

type OrderState =
    | Draft of items: (string * Quantity) list
    | Placed of items: (string * Quantity) list * placedAt: System.DateTime
    | Shipped of trackingId: string

let place now = function
    | Draft items when not items.IsEmpty -> Ok (Placed (items, now))
    | Draft _ -> Error "no items"
    | other -> Error $"cannot place from {other}"
```
- Make illegal states unrepresentable with unions per state instead of boolean flags.
- Keep functions pure (data in, data out); do I/O at the outer layer ("functional core, imperative shell").
- Separate DTO types (serialisation shape) from domain types and map between them.
- Order the project files: Domain, then Logic, then Infrastructure, then Entry point.

## Gotchas
- Over-modelling slows teams; start with records and unions, add smart constructors for invariants that bite.
- Mapping layers need tests, since the compiler cannot check DTO to domain semantics.

## Self-check
Try to construct a `Quantity` of 0 outside its module: it fails to compile.
