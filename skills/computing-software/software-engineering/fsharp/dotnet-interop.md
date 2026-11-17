---
id: computing-software.software-engineering.fsharp.dotnet-interop
name: dotnet-interop
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, dotnet-interop, fsharp-interop, out-parameters, optional-arguments]
level: practitioner
status: draft
description: "Call .NET APIs from F# handling out parameters, named and optional arguments, params, overloads and delegates."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling .NET from F#
**Goal:** use C# libraries idiomatically.

```fsharp
open System
open System.Collections.Generic

let ok, n = Int32.TryParse "12"                      // out param -> tuple
let d = Dictionary<string,int>()
d.["a"] <- 1
match d.TryGetValue "a" with | true, v -> v | _ -> 0

let dt = DateTime(2026, 11, 2)
let s = String.Join(", ", [| "a"; "b" |])            // params array
let t = TimeSpan.FromSeconds(1.5)
let msg = String.Format("{0}-{1}", 1, 2)
let rd = Console.ReadLine()                           // may be null
let f = Func<int,int>(fun x -> x + 1)                 // delegate from lambda
let l = List<int>([ 1; 2; 3 ])
l.ForEach(Action<int>(fun x -> printfn "%d" x))
let t2 = System.Threading.Tasks.Task.Run(fun () -> 42)
```
- Methods with trailing `out` parameters can be called by omitting them; you get a tuple back.
- Named arguments: `obj.Method(arg1 = 1, arg2 = 2)`; optional arguments may be omitted.
- Lambdas convert to delegates at method calls automatically; use `Func<_,_>(...)` when assigning to a value.
- F# list `[1;2]` implements `IEnumerable<T>`, so can be passed where `seq` or `IEnumerable` is expected.
- Use `ResizeArray<T>` as the F# alias of `List<T>`.

## Gotchas
- .NET methods are tupled; they do not curry, so they pipe via a lambda.
- `null` flows in from .NET: guard with `isNull`/`Option.ofObj`.

## Self-check
`Int32.TryParse "x"` gives `(false, 0)`.
