---
id: computing-software.software-engineering.fsharp.giraffe-handlers
name: giraffe-handlers
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, giraffe-handlers, fsharp-web-server, giraffe, httphandler]
level: practitioner
status: draft
description: "Build web apps with Giraffe HttpHandlers composed with >=> and choose, parsing routes and binding JSON."
sources:
  - https://github.com/giraffe-fsharp/Giraffe
  - https://learn.microsoft.com/en-us/aspnet/core/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Giraffe
**Goal:** functional web routing on ASP.NET Core.

```fsharp
open Microsoft.AspNetCore.Builder
open Microsoft.Extensions.DependencyInjection
open Giraffe

let webApp =
    choose [
        GET >=> choose [
            route "/" >=> text "hello"
            routef "/hello/%s" (fun name -> text $"Hello {name}")
            route "/people" >=> json [ {| Name = "Ada" |} ]
        ]
        POST >=> route "/echo" >=> bindJson<{| Msg: string |}> (fun m -> json m)
        setStatusCode 404 >=> text "Not found"
    ]

[<EntryPoint>]
let main args =
    let builder = WebApplication.CreateBuilder(args)
    builder.Services.AddGiraffe() |> ignore
    let app = builder.Build()
    app.UseGiraffe webApp
    app.Run()
    0
```
- A `HttpHandler` is `HttpFunc -> HttpContext -> Task<HttpContext option>`; `>=>` composes handlers, `choose` tries alternatives in order.
- `routef` supports format specifiers such as `%s`, `%i`, `%O`; `subRoute` mounts prefixes.
- Add Giraffe via the `Giraffe` NuGet package; the template ships with `dotnet new` if installed.
- Access services in handlers via `ctx.GetService<T>()`.
- `bindJson` needs a type System.Text.Json (or Newtonsoft, configurable) can deserialise.

## Gotchas
- Order matters in `choose`; place specific routes before catch-alls.
- Exceptions need an error handler registered through `app.UseGiraffeErrorHandler`.

## Self-check
`curl localhost:5000/hello/ada` prints "Hello ada" (port from launch profile).
