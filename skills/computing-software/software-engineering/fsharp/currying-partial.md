---
id: computing-software.software-engineering.fsharp.currying-partial
name: currying-partial
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, currying-partial, fsharp-functions, partial-application, higher-order]
level: intro
status: docs-checked
description: "Define curried F# functions, partially apply them and compose with pipelines and composition operators."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/tour
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Currying and partial application
**Goal:** exploit that every F# function takes one argument.

```fsharp
let add x y = x + y          // int -> int -> int
let add5 = add 5             // partial application
[1;2;3] |> List.map add5     // [6;7;8]

let inc = (+) 1
let incThenDouble = inc >> (*) 2   // forward composition: inc then double
let doubleThenInc = inc << (*) 2   // backward composition: double then inc

let total = [1;2;3;4] |> List.filter (fun n -> n % 2 = 0) |> List.sum
```
- `>>` takes two functions and returns a function; `|>` by contrast takes a value and a function (Functions page).
- Partial application means supplying fewer arguments than a curried function takes, which gives a new function.

## Gotchas
- Value restriction: a partially applied or composed value such as `let maxhash = max << hash` is not generalised; write the argument explicitly (`let maxhash obj = (max << hash) obj`).

## Self-check
`List.map (add 1) [1;2]` yields `[2;3]`.

## Checked
2026-11-03. Confirmed against the Functions language-reference page (curried functions, partial application, >> and << composition) and the Automatic Generalization page (value restriction and the maxhash fix). Removed: the sign pattern function, inference and parameter-order advice, tupled-parameter claim and the List.map value restriction example.
Method: documentation only; no commands were run.
