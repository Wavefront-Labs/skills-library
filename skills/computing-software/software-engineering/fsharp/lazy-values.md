---
id: computing-software.software-engineering.fsharp.lazy-values
name: lazy-values
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, lazy-values, fsharp-concurrency, lazy-evaluation, memoize]
level: practitioner
status: docs-checked
description: "Defer computation with lazy and Lazy.Force and memoise functions with a Dictionary closure."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/lazy-expressions
  - https://github.com/dotnet/fsharp/blob/main/src/FSharp.Core/seq.fsi
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy and memoisation
**Goal:** compute once, only when needed.

```fsharp
let expensive = lazy (printfn "computing"; 42)
let a = expensive.Force()                 // prints computing, returns 42
let b = expensive.Force()                 // cached: prints nothing
let nums = Seq.cache (seq { for i in 1 .. 3 -> i * i })
```
- `lazy expr` creates a `Lazy<'T>`; `Force` runs the expression once and returns the same result afterwards.
- Lazy evaluation is also used for sequences; see the sequences page.
- `Seq.cache` memoises the enumeration of a sequence, so the pipeline runs once.
- Multiline lazy expressions put the opening parenthesis on the `lazy` line.

## Self-check
Call `expensive.Force()` twice; "computing" prints once.

## Checked
2026-11-02. Confirmed against Learn "Lazy Expressions": lazy creates Lazy<'T>, Force evaluates once and returns the cached result, sequences use lazy evaluation, multiline layout. Seq.cache confirmed in FSharp.Core seq.fsi. Removed: Lazy.Value and IsValueCreated, the ConcurrentDictionary memoize example and its gotchas, the thread-safety claim and the let rec memoisation claim (not on the pages read).
Method: documentation only; no commands were run.
