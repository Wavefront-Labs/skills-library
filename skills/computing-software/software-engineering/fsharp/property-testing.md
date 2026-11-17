---
id: computing-software.software-engineering.fsharp.property-testing
name: property-testing
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, property-testing, fsharp-test-practice, fscheck, generators]
level: advanced
status: draft
description: "Express invariants as FsCheck properties, write custom generators and shrink failures."
sources:
  - https://fscheck.github.io/FsCheck/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FsCheck
**Goal:** test laws, not examples.

```fsharp
open FsCheck
open FsCheck.FSharp

let revRevIsId (xs: int list) = List.rev (List.rev xs) = xs
Check.Quick revRevIsId

let nonEmptyStrings = ArbMap.defaults |> ArbMap.generate<NonEmptyString>   // newer API; older: Arb.generate
let genPos = Gen.choose (1, 100)

let prop = Prop.forAll (Arb.fromGen genPos) (fun n -> n > 0)
Check.Quick prop

// xUnit integration
// open FsCheck.Xunit
// [<Property>] let ``rev twice`` (xs: int list) = List.rev (List.rev xs) = xs
```
- `Check.Quick` runs 100 random cases and shrinks counterexamples; `Check.QuickThrowOnFailure` for CI.
- Custom generators with `Gen.choose`, `Gen.elements`, `Gen.map`, `Gen.oneof`; register with `Arb`.
- Typical properties: round-trip (parse/print), idempotence, invariants after operations, comparison with a simple model.
- Replay a failure with the printed seed (`Config.WithReplay`).
- The `Arb.generate` vs `ArbMap` API changed between FsCheck 2 and 3 (unconfirmed exact names; check the docs for your version).

## Gotchas
- Properties must be deterministic given the input.
- Generators for recursive types need `Gen.sized` to bound depth.

## Self-check
Write a deliberately false property and observe a shrunk small counterexample.
