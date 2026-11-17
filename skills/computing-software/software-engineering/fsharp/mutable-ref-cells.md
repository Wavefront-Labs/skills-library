---
id: computing-software.software-engineering.fsharp.mutable-ref-cells
name: mutable-ref-cells
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, mutable-ref-cells, fsharp-bindings, ref-cells, mutable]
level: practitioner
status: docs-checked
description: "Mutate local state with let mutable, and use ref cells when a closure must share mutable state."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/values/
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/reference-cells
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# mutable and ref cells
**Goal:** mutate state with the right construct for the scope.

```fsharp
let mutable count = 0
count <- count + 1

let makeCounter () =
    let mutable n = 0
    fun () -> n <- n + 1; n          // n is promoted to a ref cell by the compiler

let r = ref 10                       // explicit ref cell
r.Value <- 11                        // preferred over legacy ! and :=
```
- `let mutable` declares a value that can be changed; keep its scope limited, as a field or a local.
- A mutable value captured by a closure (including seq builders) is automatically promoted to a `ref` cell.
- `ref` creates a reference cell whose underlying value is read and set with `.Value`.
- The `!` and `:=` operators are deprecated since F# 6 and give informational warnings.
- Record fields can be declared `mutable`: `{ mutable Count: int }`.

## Self-check
After `r.Value <- 11`, `r.Value` reads 11.

## Checked
2026-11-02. Confirmed against Learn "Values" (mutable variables; a captured mutable value may be promoted to a ref cell) and "Reference Cells" (ref, .Value, deprecated ! and := since F# 6 with informational warnings, mutable record fields). Corrected: the claim that a closure cannot capture a let mutable (FS0407) contradicts the page, so it is removed. Removed: the idiom advice on folds and recursion, the module-level static field and the ref cell thread-safety claims (not on the pages read).
Method: documentation only; no commands were run.
