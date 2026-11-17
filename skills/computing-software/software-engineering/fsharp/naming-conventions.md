---
id: computing-software.software-engineering.fsharp.naming-conventions
name: naming-conventions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, naming-conventions, fsharp-style, pascalcase-camelcase, naming-style]
level: intro
status: draft
description: "Apply the F# naming conventions for types, modules, values, parameters, union cases and generic parameters."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Naming conventions
**Goal:** names that match the F# ecosystem.

```fsharp
namespace Acme.Billing                          // PascalCase namespaces

type InvoiceLine = { UnitPrice: decimal }       // PascalCase types and record fields
type PaymentState = Pending | Paid              // PascalCase union cases
module InvoiceCalc =                            // PascalCase modules
    let totalPrice (lines: InvoiceLine list) =  // camelCase functions and values
        lines |> List.sumBy (fun l -> l.UnitPrice)
type Repo<'TItem> = abstract Get : int -> 'TItem  // generic params: 'T or 'TItem, short lowercase 'a in functions
```
- PascalCase: types, modules, namespaces, union cases, record fields, members, properties, enum cases, `[<Literal>]` values.
- camelCase: let-bound values and functions, parameters, local names.
- Use `'T`-prefixed names for explicit generic parameters on types and `'a`/`'b` for inferred ones.
- Avoid underscores in names, except as the discard `_` and in test names.
- Active pattern names use `(|Parse|_|)`; operators are rare.
- Acronyms: treat as words (`HttpClient`, `Id`).

## Gotchas
- Lowercase identifiers in patterns bind variables; uppercase cases/literals match constants.
- Do not use Hungarian notation or `I` prefix on non-interface types; interfaces start with `I`.

## Self-check
Run Fantomas and an analyzer or review checklist against the rules above.
