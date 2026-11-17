---
id: computing-software.software-engineering.fsharp.json-serialization
name: json-serialization
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, json-serialization, fsharp-io, system-text-json, fsharp-json]
level: practitioner
status: draft
description: "Serialise F# records, options and unions with System.Text.Json, noting what needs FSharp.SystemTextJson."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JSON in F#
**Goal:** round-trip F# data to JSON.

```fsharp
open System.Text.Json

[<CLIMutable>]
type Person = { Name: string; Age: int }

let json = JsonSerializer.Serialize { Name = "Ada"; Age = 36 }
let p = JsonSerializer.Deserialize<Person> """{"Name":"Ada","Age":36}"""

// Options, unions, and F# collections need the FSharp.SystemTextJson package
// open System.Text.Json.Serialization
let opts = JsonSerializerOptions(PropertyNameCaseInsensitive = true)
// opts.Converters.Add(JsonFSharpConverter())
let doc = JsonDocument.Parse """{"a":[1,2]}"""
let n = doc.RootElement.GetProperty("a").GetArrayLength()
```
- Plain System.Text.Json handles classes and records (records usually need `[<CLIMutable>]` or recent .NET constructor support) but not F# unions, options or `Map` in a friendly way.
- `FSharp.SystemTextJson` provides `JsonFSharpConverter` for unions, options, tuples and maps (third party package; options configurable).
- Alternatives: Thoth.Json, FSharp.Data JsonProvider, Newtonsoft with its F# converters.

## Gotchas
- Deserialising into a record with a missing field yields null/default for reference types, bypassing F# non-null expectations.
- `Option` serialises as an object unless a converter is registered.

## Self-check
Round-trip a record with an option field with and without the converter and compare outputs.
