---
id: computing-software.software-engineering.fsharp.classes-members
name: classes-members
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, classes-members, fsharp-oop, primary-constructor, auto-properties]
level: intro
status: docs-checked
description: "Define F# classes with primary constructors, let bindings, properties, methods and secondary constructors."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/classes
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Classes
**Goal:** write idiomatic F# classes.

```fsharp
type Counter(start: int) =
    let mutable count = start
    do printfn "created at %d" start          // runs in constructor
    new() = Counter(0)                         // secondary constructor
    member this.Count = count
    member this.Increment() = count <- count + 1
    member this.Reset() = count <- 0
    static member Zero = Counter()
    override this.ToString() = $"Counter({count})"

let c = Counter 5
c.Increment()
```
- The primary constructor parameters follow the type name; `let` and `do` bindings run for each instance.
- Additional constructors use `new` and must call the primary constructor.
- Members can be instance or static methods and properties; use the self identifier (`this`) to refer to the instance.

## Self-check
Create `Counter()`, increment twice and print 2.

## Checked
2026-11-02. Confirmed against Learn "Classes": primary constructor, let and do bindings, additional constructors with new, self identifiers, static and instance members. Removed: the reference-equality bullet, member val auto-properties, static let, optional-argument parameters, the IDisposable constructor warning and the underscore self-identifier claim (not on the page; examples use this).
Method: documentation only; no commands were run.
