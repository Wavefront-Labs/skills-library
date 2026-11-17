---
id: computing-software.software-engineering.fsharp.test-doubles
name: test-doubles
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, test-doubles, fsharp-test-practice, stubs-by-functions, dependency-rejection]
level: practitioner
status: draft
description: "Test F# code by passing functions and records of functions as fakes instead of using mocking frameworks."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test doubles without mocks
**Goal:** keep I/O at the edge, test pure logic directly.

```fsharp
type Deps =
    { Now: unit -> System.DateTime
      Save: string -> Async<unit> }

let register deps name = async {
    if name = "" then return Error "empty"
    else
        do! deps.Save $"{name}@{deps.Now()}"
        return Ok name
}

[<Fact>]
let ``register saves`` () = async {
    let saved = ResizeArray<string>()
    let deps =
        { Now = fun () -> System.DateTime(2026, 1, 1)
          Save = fun s -> async { saved.Add s } }
    let! r = register deps "ada"
    Assert.Equal(Ok "ada", r)
    Assert.Single saved |> ignore
} |> Async.RunSynchronously
```
- Prefer pure functions; where effects are needed, take them as parameters (record of functions or interface).
- For interfaces consumed from C# libraries, use object expressions (`{ new IFoo with ... }`) as stubs.
- Mocking frameworks (Moq, NSubstitute, Foq) work but need care with F# types; most F# teams avoid them.

## Gotchas
- Time and randomness are dependencies too; inject them.
- Do not test private helpers; test through the public function.

## Self-check
The test above runs with no database and no clock dependencies.
