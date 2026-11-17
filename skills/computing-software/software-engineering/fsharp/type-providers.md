---
id: computing-software.software-engineering.fsharp.type-providers
name: type-providers
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, type-providers, fsharp-metaprogramming, type-provider, erased-types]
level: advanced
status: draft
description: "Consume type providers such as FSharp.Data to get compile-time typed access to data schemas and understand their tooling limits."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
  - https://fsprojects.github.io/FSharp.Data/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type providers
**Goal:** get typed access to external schemas.

```fsharp
#r "nuget: FSharp.Data"
open FSharp.Data

type Weather = JsonProvider<"""{ "temp": 12.5, "city": "Oslo" }""">
let w = Weather.Parse """{ "temp": 20.0, "city": "Rome" }"""
printfn "%s %f" w.City w.Temp

type Csv = CsvProvider<"data/sample.csv", HasHeaders=true>
let rows = Csv.Load("data/prod.csv").Rows |> Seq.map (fun r -> r.Id)
```
- A type provider generates types at compile time from a sample/schema (JSON, CSV, XML, SQL, OpenAPI, ...); the IDE completes members from the sample.
- Static parameters (the angle-bracket arguments) must be compile-time constants; use `[<Literal>]` paths.
- Providers load inside the compiler and IDE, so they can be fragile with `dotnet build` on new SDKs or in `net` target mismatches.
- Sample drives the shape: a field missing from the sample is not available; use a representative or multi-sample file.

## Gotchas
- Relative sample paths resolve against the project directory (`ResolutionFolder`).
- Slow providers slow compile and IDE responsiveness; prefer runtime parsing in hot builds.

## Self-check
Change the sample field name and confirm the usage site fails to compile.
