---
id: computing-software.software-engineering.fsharp.try-with-failwith
name: try-with-failwith
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, try-with-failwith, fsharp-exceptions, custom-exceptions, reraise]
level: intro
status: docs-checked
description: "Raise and handle exceptions with failwith, raise, try/with, try/finally, and define F# exception types."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions
**Goal:** handle exceptional conditions properly.

```fsharp
exception NotFound of string                        // F# exception type
exception Invalid of code: int * msg: string

let find k = failwith $"missing {k}"                 // throws System.Exception
let f () = raise (NotFound "id1")
let g () = invalidArg "x" "bad"                      // ArgumentException
let h x = if x < 0 then invalidOp "negative"         // InvalidOperationException

let safe () =
    try
        f ()
    with
    | NotFound id -> printfn "nf %s" id
    | :? System.ArgumentException as e -> printfn "%s" e.Message
    | ex when ex.Message.Contains "x" -> reraise ()   // keeps stack trace
    | _ -> ()

try (try failwith "a" finally printfn "cleanup") with _ -> ()
let r = try Some (int "x") with _ -> None
```
- `try/with` and `try/finally` are separate expressions; nest them when you need both.
- An F# exception defined with `exception` is a new type that inherits from `System.Exception`.
- `try...with` patterns: `:? Type`, `:? Type as id`, `ExceptionName(args)`, `identifier` (any exception) and `identifier when condition`.
- In `async`, `task` and other computation expressions a customised `try...with` is used.

## Gotchas
- A catch-all handler hides bugs; log or rethrow.

## Self-check
`try failwith "x" with e -> e.Message` is `"x"`.

## Checked
2026-11-03. Confirmed against the Exception handling pages: try...with, try...finally, Exception Types, failwith, raise, invalidArg. Removed: reraise semantics, `raise ex` stack-trace claim, failwithf/nullArg/invalidOp mapping, structural-equality claim and the seq/async timing claim.
Method: documentation only; no commands were run.
