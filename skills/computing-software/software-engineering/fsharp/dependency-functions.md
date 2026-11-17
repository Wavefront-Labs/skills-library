---
id: computing-software.software-engineering.fsharp.dependency-functions
name: dependency-functions
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, dependency-functions, fsharp-architecture, partial-application-di, reader-pattern]
level: practitioner
status: draft
description: "Pass dependencies as function parameters, partially apply at the composition root, and bridge to DI containers."
sources:
  - https://learn.microsoft.com/en-us/dotnet/fsharp/style-guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependencies as functions
**Goal:** inject without a container.

```fsharp
// domain function takes its dependencies first, so it partially applies
let register (save: string -> Async<unit>) (now: unit -> System.DateTime) name = async {
    do! save $"{name}@{now ()}"
}

// composition root
let saveToDb s = async { () }
let registerUser = register saveToDb (fun () -> System.DateTime.UtcNow)

// bridging to ASP.NET Core DI
// builder.Services.AddSingleton<UserRegistration>(fun sp -> registerUser)
```
- Put dependencies as leading curried parameters and the data last, so `register deps` yields the dependency-free function.
- For many dependencies, group them in a record (`Deps`) and pass it.
- Use the host's DI (`IServiceProvider`) only at the entry point (Giraffe's `ctx.GetService<T>()`).
- Resist generic DI frameworks and Reader monads unless the team knows them.

## Gotchas
- Partial application of methods requires an F# function wrapper.
- Singletons capturing scoped services (DbContext) cause lifetime bugs in ASP.NET.

## Self-check
Call `registerUser "ada"` in a test using fake `save` and `now`.
