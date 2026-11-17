---
id: computing-software.software-engineering.fsharp.unquote-fsunit
name: unquote-fsunit
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, unquote-fsunit, fsharp-test-frameworks, unquote, fsunit]
level: practitioner
status: draft
description: "Write expressive assertions using Unquote quotation-based tests and FsUnit's should syntax."
sources:
  - https://xunit.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unquote and FsUnit
**Goal:** readable failure messages.

```fsharp
open Swensen.Unquote

[<Fact>]
let ``sum`` () =
    test <@ List.sum [1; 2; 3] = 6 @>
    raises<System.DivideByZeroException> <@ 1 / 0 @>

// FsUnit
open FsUnit.Xunit
[<Fact>]
let ``fsunit`` () =
    [1; 2; 3] |> List.length |> should equal 3
    "abc" |> should startWith "a"
    None |> should equal None
```
- Unquote's `test <@ expr @>` evaluates the quotation and prints a step-by-step reduction on failure.
- `=!` operator: `actual =! expected`.
- FsUnit offers `should equal`, `should be (greaterThan 3)`, `should haveLength`, `should throw typeof<...>` flavours per test framework package (`FsUnit.Xunit`, `FsUnit.NUnit`).
- Pick one assertion library per project.

## Gotchas
- Quotation evaluation is slower; fine for tests.
- FsUnit `should equal` uses `Equals`, not custom comparers.

## Self-check
Fail a Unquote test intentionally and read the reduction steps.
