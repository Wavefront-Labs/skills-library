---
id: computing-software.software-engineering.fsharp.recursion-tailcalls
name: recursion-tailcalls
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, recursion-tailcalls, fsharp-functions, tail-recursion, let-rec]
level: practitioner
status: docs-checked
description: "Write let rec and mutually recursive functions with accumulators so the compiler emits tail calls or loops."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursion and tail calls
**Goal:** recurse without stack overflow.

```fsharp
let rec factorial n acc =
    if n <= 1I then acc else factorial (n - 1I) (acc * n)   // tail call

let rec isEven n = if n = 0 then true  else isOdd (n - 1)
and     isOdd  n = if n = 0 then false else isEven (n - 1)

let sumList xs =
    let rec go acc = function
        | []      -> acc
        | x :: tl -> go (acc + x) tl
    go 0 xs
```
- `let rec` is required for a function to call itself; `and` chains mutual recursion.
- A tail-recursive function lets the compiler optimise the code to be as fast as a `while` loop; accumulator parameters carry intermediate values.
- A non-tail-recursive definition such as `fib (n-1) + fib (n-2)` needs the call stack; refactor with an inner `loop` function and accumulators.
- From F# 8.0 the `[<TailCall>]` attribute makes the compiler warn about non-tail recursive calls.
- Methods are implicitly recursive within their type; `let` bindings inside classes still need `rec`.

## Gotchas
- Naive recursion recomputes values (the Fibonacci example on the page); prefer an accumulator version.

## Self-check
Add `[<TailCall>]` (F# 8+) to `factorial` and `sumList` and confirm the compiler gives no warning.

## Checked
2026-11-03. Confirmed against the Recursive Functions: the rec Keyword page (rec, and, accumulators, TailCall from F# 8.0, implicit method recursion) and the Compiler options page. Removed: the IL .tail and Debug/Release claims, the try/use and byref non-tail claims and the `-c Release` advice.
Method: documentation only; no commands were run.
