---
id: computing-software.software-engineering.fsharp.csharp-consumption
name: csharp-consumption
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, csharp-consumption, fsharp-interop, library-design, compiled-api]
level: advanced
status: draft
description: "Shape public F# APIs for C# consumers: tupled members, CLIMutable, avoiding curried and F#-only types."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# F# libraries consumed from C#
**Goal:** make the public surface friendly to other .NET languages.

```fsharp
namespace MyLib

open System.Runtime.CompilerServices

type Calculator() =
    member _.Add(a: int, b: int) = a + b                       // tupled -> normal C# method
    member _.Opt(?x: int) = defaultArg x 0                    // C# sees an FSharpOption parameter
    member _.Handler : System.Func<int,int> = System.Func<_,_>(fun x -> x)

[<CLIMutable>] type Dto = { Id: int; Name: string }

module Util =
    [<CompiledName("Double")>]
    let double x = x * 2
```
- Expose classes with tupled methods, `Func`/`Action`, `Task`, `IEnumerable<T>`/`IReadOnlyList<T>`; avoid curried functions, `option`, `list`, `Async`, unions and units in the public API.
- Module functions compile to static methods of a static class; the module name becomes the class name.
- The style guide recommends wrapper types or a thin adapter layer for C# callers.
- Use `[<Extension>]` for extension methods; `[<CompiledName>]` for .NET naming.

## Gotchas
- F# `?x` optional parameters surface as `FSharpOption<T>` in C#; for C#-style optionals use `[<Optional; DefaultParameterValue(0)>]` from System.Runtime.InteropServices.
- Records expose properties but constructors take all fields in order; reordering fields is a breaking change.

## Self-check
Reference the compiled DLL from a C# project and call `Add`; check IntelliSense shows plain types.
