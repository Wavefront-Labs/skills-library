---
id: computing-software.software-engineering.fsharp.fsharp-data-parsing
name: fsharp-data-parsing
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, fsharp-data-parsing, fsharp-data, csv-parsing, http-utilities]
level: practitioner
status: draft
description: "Parse CSV, JSON, XML and HTML and make HTTP calls with the FSharp.Data library."
sources:
  - https://fsprojects.github.io/FSharp.Data/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FSharp.Data
**Goal:** read semi-structured data quickly.

```fsharp
#r "nuget: FSharp.Data"
open FSharp.Data
open FSharp.Data.JsonExtensions

let csv = CsvFile.Load("data.csv").Cache()
for row in csv.Rows do printfn "%s" (row.GetColumn "name")

let json = JsonValue.Parse """{ "items": [1, 2, 3] }"""
let items = json.["items"].AsArray() |> Array.map (fun v -> v.AsInteger())

let body = Http.RequestString("https://example.com", headers = [ "Accept", "text/html" ])

let html = HtmlDocument.Load "https://example.com"
let links = html.Descendants "a" |> Seq.choose (fun a -> a.TryGetAttribute "href") |> Seq.map (fun a -> a.Value())
```
- Runtime types (`CsvFile`, `JsonValue`, `HtmlDocument`, `Http`) work without type providers; type providers give typed access if you have a sample.
- Use `HttpClient` for production services; `Http.*` helpers are for scripts and small tools.
- Large CSV files: use `CsvFile.Load` lazily without `.Cache()` unless you iterate twice.
- `AsArray`, `AsInteger` and the `.["key"]` indexer come from `FSharp.Data.JsonExtensions`; unconfirmed whether newer versions changed this, check the docs.

## Gotchas
- Type inference of CSV columns depends on the sample rows.
- HTML parsing is lenient but not a browser.

## Self-check
Parse a tiny JSON string and read an integer property.
