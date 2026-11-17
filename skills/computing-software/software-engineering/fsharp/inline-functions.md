---
id: computing-software.software-engineering.fsharp.inline-functions
name: inline-functions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, inline-functions, fsharp-functions, inline, srtp]
level: advanced
status: docs-checked
description: "Use inline functions and statically resolved type parameters for generic arithmetic and member constraints."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inline and SRTP
**Goal:** write generic code over operators and members without boxing.

```fsharp
let inline add x y = x + y
let a = add 1 2
let b = add 1.5 2.5

let inline sumBy ([<InlineIfLambda>] f: 'a -> ^b) (xs: 'a list) : ^b =
    let mutable acc = LanguagePrimitives.GenericZero< ^b >
    for x in xs do acc <- acc + f x
    acc

// member constraint
let inline lengthOf (x: ^T) = (^T : (member Length : int) x)
let n = lengthOf "abc"
```
- Inline functions are integrated directly into the calling code; statically resolved type parameters (`^T`, or `'T` from F# 7) are replaced by real types at compile time and need `inline`.
- Avoid `inline` for optimisation unless other techniques have failed; overuse makes code less resistant to compiler and library changes.
- `[<InlineIfLambda>]` makes the compiler inline a lambda argument at the call site; the opt-in warning 3517 flags call sites where it is not bound to a lambda.
- `LanguagePrimitives.GenericZero` gives a numeric zero for generic code.

## Gotchas
- Statically resolved type parameters cannot be used on functions or methods that are not inline.

## Self-check
`add 1 2 = 3` and `add 1.5 2.5 = 4.0` both compile from one definition.

## Checked
2026-11-03. Confirmed against the Inline Functions page (InlineIfLambda, warning 3517, overuse caution) and the Statically Resolved Type Parameters page (compile-time resolution, member constraints, inline requirement, F# 7 syntax) and the FSharp.Core LanguagePrimitives reference (GenericZero). Removed: the reflection and code-bloat claim, the SRTP-error advice, the generic-math remark and the F# 6 version note.
Method: documentation only; no commands were run.
