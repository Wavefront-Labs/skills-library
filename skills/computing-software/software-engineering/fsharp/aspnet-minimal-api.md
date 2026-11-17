---
id: computing-software.software-engineering.fsharp.aspnet-minimal-api
name: aspnet-minimal-api
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, aspnet-minimal-api, fsharp-web-server, minimal-api, webapplication]
level: practitioner
status: draft
description: "Write ASP.NET Core minimal APIs in F# with MapGet and MapPost, dependency injection, and the F# type inference caveats."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Minimal APIs in F#
**Goal:** a web service without extra framework.

```fsharp
open System
open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Http
open Microsoft.Extensions.DependencyInjection

[<CLIMutable>]
type Item = { Id: int; Name: string }

[<EntryPoint>]
let main args =
    let builder = WebApplication.CreateBuilder(args)
    builder.Services.AddSingleton<TimeProvider>(TimeProvider.System) |> ignore
    let app = builder.Build()

    app.MapGet("/", Func<string>(fun () -> "hi")) |> ignore
    app.MapGet("/items/{id}", Func<int, IResult>(fun id -> Results.Ok { Id = id; Name = "x" })) |> ignore
    app.MapPost("/items", Func<Item, IResult>(fun item -> Results.Created($"/items/{item.Id}", item))) |> ignore
    app.Run()
    0
```
- Lambdas must be wrapped in `Func<..>`/`Action<..>` delegates for the `Map*` methods.
- Use `[<CLIMutable>]` records for request body binding.
- F# async results: return `Task<IResult>` (use `task { }`) rather than `Async`.
- Dependency injection works through parameter types of the delegate.
- Unconfirmed: F# 9/ASP.NET 9 may offer smoother lambda conversion; the explicit `Func<_>` form is safe.

## Gotchas
- Without `CLIMutable`, model binding may fail for records.
- `app.Run()` blocks; put registrations before it.

## Self-check
`curl localhost:5000/items/3` returns JSON for id 3.
