---
id: computing-software.software-engineering.fsharp.xunit-tests
name: xunit-tests
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, xunit-tests, fsharp-test-frameworks, xunit, theory-inlinedata]
level: practitioner
status: draft
description: "Write xUnit Facts and Theories in F# with the dotnet test template and attribute data."
sources:
  - https://xunit.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# xUnit in F#
**Goal:** use the standard .NET runner.

```bash
dotnet new xunit -lang "F#" -o Tests
dotnet test
```
```fsharp
module Tests

open Xunit

[<Fact>]
let ``adds numbers`` () =
    Assert.Equal(2, 1 + 1)

[<Theory>]
[<InlineData(1, 2)>]
[<InlineData(2, 3)>]
let ``increments`` (input: int, expected: int) =
    Assert.Equal(expected, input + 1)

[<Fact>]
let ``throws`` () =
    Assert.Throws<System.ArgumentException>(fun () -> invalidArg "x" "bad" |> ignore) |> ignore
```
- Double-backtick names give readable test names.
- `[<MemberData>]` and `[<ClassData>]` for richer data; F# lists of obj arrays work.
- Tests are module functions; `[<Fact>]` methods must take unit or parameters via Theory.
- Use `FsUnit.Xunit` for `|> should equal` syntax.

## Gotchas
- Test methods in an F# module are static; xUnit creates a class instance per test only for class-based tests.
- Assertions must return unit (`|> ignore` after `Assert.Throws`).

## Self-check
`dotnet test` reports 3 passed.
