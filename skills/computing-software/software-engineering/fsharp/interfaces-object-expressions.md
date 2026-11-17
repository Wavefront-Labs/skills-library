---
id: computing-software.software-engineering.fsharp.interfaces-object-expressions
name: interfaces-object-expressions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, interfaces-object-expressions, fsharp-oop, object-expressions, interface-implementation]
level: practitioner
status: docs-checked
description: "Declare and implement interfaces explicitly and create anonymous implementations with object expressions."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/interfaces
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/object-expressions
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Interfaces and object expressions
**Goal:** abstract behaviour without a class hierarchy.

```fsharp
type IShape =
    abstract Area : unit -> float
    abstract Name : string

type Square(side: float) =
    interface IShape with
        member this.Area() = side * side
        member this.Name = "square"

let s = Square 2.0
let area = (s :> IShape).Area()          // interface members need an upcast
let unit : IShape =                       // object expression
    { new IShape with
        member this.Area() = 1.0
        member this.Name = "unit" }
let d = { new System.IDisposable with member this.Dispose() = printfn "bye" }
```
- Interface members are implemented inside an `interface IFoo with` block.
- Interface methods can be called only through the interface, so an upcast is needed.
- An object expression implements one or more interfaces, or overrides members of a base class, without a named type.

## Self-check
Call `Area()` through an `IShape` upcast and through the object expression.

## Checked
2026-11-02. Confirmed against Learn "Interfaces (F#)" (interface ... with implementations, abstract members, upcast to call interface methods, upcast with `:>`, marker interfaces) and "Object Expressions" (implementing one or more interfaces, overriding base members). Removed: the no-default-implementations claim (the page shows F# consuming C# default members), the records-of-functions advice, the C# default-member bullet and the 'member not found' gotcha wording (not on the pages read).
Method: documentation only; no commands were run.
