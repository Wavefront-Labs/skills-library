---
id: computing-software.software-engineering.fsharp.regex-text
name: regex-text
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, regex-text, fsharp-io, regex, regex-active-pattern]
level: practitioner
status: draft
description: "Use System.Text.RegularExpressions in F# and wrap Regex in an active pattern for readable matching."
sources:
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regex in F#
**Goal:** parse text with regular expressions.

```fsharp
open System.Text.RegularExpressions

let (|Match|_|) pattern input =
    let m = Regex.Match(input, pattern)
    if m.Success then Some [ for g in m.Groups -> g.Value ] else None

match "2026-11-02" with
| Match @"^(\d{4})-(\d{2})-(\d{2})$" [ _; y; mo; d ] -> printfn "%s %s %s" y mo d
| _ -> printfn "no match"

let all = Regex.Matches("a1b22", @"\d+") |> Seq.map (fun m -> m.Value) |> Seq.toList
let replaced = Regex.Replace("a  b", @"\s+", " ")
let rx = Regex(@"\d+", RegexOptions.Compiled ||| RegexOptions.CultureInvariant)
let named = Regex.Match("k=v", @"(?<key>\w+)=(?<val>\w+)").Groups.["key"].Value
```
- Use verbatim `@"..."` or triple-quoted strings to avoid doubling backslashes.
- `Regex` static methods cache patterns; construct and reuse an instance (`RegexOptions.Compiled`) for hot code.
- Pass a `matchTimeout` for untrusted input to bound catastrophic backtracking.
- Group 0 is the full match.

## Gotchas
- `m.Groups` enumerates `Group` in newer .NET; older frameworks need `Seq.cast<Group>`.
- Greedy patterns on user-controlled text can be a denial-of-service vector.

## Self-check
The active pattern above extracts `["2026-11-02"; "2026"; "11"; "02"]` from the date.
