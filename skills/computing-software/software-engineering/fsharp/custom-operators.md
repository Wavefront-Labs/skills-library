---
id: computing-software.software-engineering.fsharp.custom-operators
name: custom-operators
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, custom-operators, fsharp-functions, operator-overloading]
level: practitioner
status: draft
description: "Define custom infix and prefix operators in F# and overload operators on types, with precedence from the leading characters."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom operators
**Goal:** add operators without surprising precedence.

```fsharp
let (|+|) a b = a + b * 2       // custom infix; precedence from leading char
let (!!) x = not x               // prefix operators start with ! or ~
let (>>=) m f = Option.bind f m  // classic bind operator

type Vec =
    { X: float; Y: float }
    static member (+) (a: Vec, b: Vec) = { X = a.X + b.X; Y = a.Y + b.Y }
    static member (*) (k: float, v: Vec) = { X = k * v.X; Y = k * v.Y }
    static member (~-) (v: Vec) = { X = -v.X; Y = -v.Y }

let v = { X = 1.; Y = 2. } + { X = 3.; Y = 4. }
```
- Operator characters: `! % & * + - . / < = > ? @ ^ | ~`. Precedence and associativity come from the leading characters (see the operator precedence table in the language reference).
- Wrap the operator in parentheses to define it or pass it as a function: `List.reduce (+) xs`.

## Gotchas
- Writing the multiplication operator as a function needs spaces, `( * )`, because `(*` starts a comment.
- Too many custom operators hurt readability; the style guide advises restraint.

## Self-check
`{X=1.;Y=1.} + {X=1.;Y=1.}` evaluates to `{X=2.;Y=2.}`.
