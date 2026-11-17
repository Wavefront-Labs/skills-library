---
id: computing-software.software-engineering.fsharp.attributes-interop
name: attributes-interop
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, attributes-interop, fsharp-metaprogramming, entrypoint, compiled-name]
level: practitioner
status: draft
description: "Apply attributes such as EntryPoint, CompiledName, Literal, AutoOpen and Obsolete for entry, naming and interop."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attributes
**Goal:** know the everyday F# attributes.

```fsharp
[<EntryPoint>]
let main argv =
    printfn "args: %A" argv
    0                                     // exit code

[<Literal>]
let Port = 8080                           // usable in patterns and attribute arguments

[<CompiledName("DoWork")>]
let doWork x = x                          // .NET name for C# callers

[<Obsolete("use Other")>]
let old () = ()

[<System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.NoInlining)>]
let slow () = ()

[<Struct>] type S = { A: int }
[<CLIMutable>] type Dto = { Name: string }   // parameterless ctor + setters for serialisers/ORMs
[<DefaultValue>] val mutable Field: int       // inside a class with primary constructor
```
- `[<EntryPoint>]` must be on the last function of the last file and take `string[]`.
- `[<CLIMutable>]` is the usual fix for model binders and EF/JSON libraries that need default constructors.
- `[<Literal>]` names must start uppercase to be usable in patterns.
- Multiple attributes: `[<A; B>]`.

## Gotchas
- `[<EntryPoint>]` plus top-level statements in the same last file is an error.
- Attribute arguments must be constants or literals.

## Self-check
Compile a console app with `[<EntryPoint>]` and run `dotnet run -- a b`.
