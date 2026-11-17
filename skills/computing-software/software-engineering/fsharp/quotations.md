---
id: computing-software.software-engineering.fsharp.quotations
name: quotations
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, quotations, fsharp-metaprogramming, code-quotations, reflection]
level: advanced
status: draft
description: "Capture F# code as data with quotations, splice values, and use Reflection helpers for unions and records."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quotations and reflection
**Goal:** inspect or transform code as a tree.

```fsharp
open Microsoft.FSharp.Quotations
open Microsoft.FSharp.Quotations.Patterns
open Microsoft.FSharp.Reflection

let q = <@ 1 + 2 @>                          // Expr<int>
let name = <@@ System.Math.Abs(-1) @@>        // untyped Expr
let n = 5
let spliced = <@ %%(Expr.Value 1) + n @>      // %% typed splice; n captured as value

match q.Raw with
| Call (_, mi, args) -> printfn "%s" mi.Name
| _ -> ()

let cases = FSharpType.GetUnionCases typeof<option<int>>
let isU = FSharpType.IsUnion typeof<option<int>>
let v = FSharpValue.MakeUnion(cases.[1], [| box 3 |])
```
- Typed `<@ @>` and untyped `<@@ @@>` quotations; `%` and `%%` splice.
- Evaluating quotations needs a library (for example FSharp.Linq.RuntimeHelpers.LeafExpressionConverter or third-party evaluators); the core only constructs and inspects them.
- Use cases: Unquote assertions, web frameworks, SQL translation, Fable plugins.

## Gotchas
- Reflection over unions/records is slow; cache `FSharpType` results.
- Inline functions inside quotations are not always preserved.

## Self-check
Print the `Call` pattern method name for `<@ List.length [1] @>`.
