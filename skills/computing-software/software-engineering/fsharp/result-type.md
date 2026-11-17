---
id: computing-software.software-engineering.fsharp.result-type
name: result-type
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, result-type, fsharp-option-result, railway-oriented, result-module]
level: practitioner
status: docs-checked
description: "Handle expected failures with Result, Result.map and bind, and collect errors without exceptions."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/results
  - https://github.com/dotnet/fsharp/blob/main/src/FSharp.Core/result.fsi
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Result
**Goal:** make failure explicit in the type.

```fsharp
type ParseError = Empty | NotANumber of string

let parse (s: string) : Result<int, ParseError> =
    if System.String.IsNullOrWhiteSpace s then Error Empty
    else
        match System.Int32.TryParse s with
        | true, v -> Ok v
        | _ -> Error (NotANumber s)

let doubled = parse "21" |> Result.map ((*) 2)               // Ok 42
let chained = parse "4" |> Result.bind (fun n -> if n > 0 then Ok n else Error Empty)
let withMsg = parse "x" |> Result.mapError string
let v = parse "9" |> Result.defaultValue 0
// collect a list of Results: stop at the first Error
let all =
    [ "1"; "2" ]
    |> List.map parse
    |> List.fold (fun acc r -> acc |> Result.bind (fun xs -> r |> Result.map (fun x -> x :: xs))) (Ok [])
    |> Result.map List.rev
```
- `Result<'T,'TError>` is the union `Ok | Error`, used for railway-style error handling.
- Module members include `map`, `mapError`, `bind`, `isOk`, `isError`, `defaultValue` and `defaultWith`.

## Self-check
`parse "abc"` returns `Error (NotANumber "abc")`.

## Checked
2026-11-02. Confirmed against Learn "Results" (Ok and Error union, railway-style use) and FSharp.Core result.fsi: map, mapError, bind, isOk, isError, defaultValue, defaultWith. Removed: the error-union-per-layer and exceptions-versus-Result advice, the F# 8 version tag, the FsToolkit.ErrorHandling claims and the `result { }` builder line (third-party, not read).
Method: documentation only; no commands were run.
