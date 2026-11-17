---
id: computing-software.software-engineering.fsharp.logging-config
name: logging-config
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, logging-config, fsharp-architecture, ilogger, structured-logging]
level: practitioner
status: draft
description: "Log from F# with ILogger structured templates, log levels and avoiding sprintf in logging calls."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/
  - https://learn.microsoft.com/en-us/dotnet/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging
**Goal:** structured logs that tools can query.

```fsharp
open Microsoft.Extensions.Logging

let handle (logger: ILogger) (userId: int) =
    logger.LogInformation("Handling user {UserId}", userId)
    try
        ()
    with ex ->
        logger.LogError(ex, "Failed for user {UserId}", userId)
        reraise ()
```
- Use message templates with named placeholders, not `$"..."` or `sprintf`, so the structured values stay queryable (interpolation loses structure and allocates).
- Levels: Trace, Debug, Information, Warning, Error, Critical; set via configuration (`Logging:LogLevel:Default`).
- Obtain `ILogger<T>` from DI; in scripts create a factory with `LoggerFactory.Create(fun b -> b.AddConsole() |> ignore)`.
- Serilog and Microsoft.Extensions.Logging interoperate for sinks (files, Seq, etc.).
- Log at boundaries; do not log and rethrow at every layer.

## Gotchas
- Logging calls with many arguments use the params overload and allocate; use `LoggerMessage` source patterns for hot paths (the generator is C#-only; define delegates with `LoggerMessage.Define` in F#).
- Never log secrets or full request bodies.

## Self-check
Run with the console provider and see `UserId` in the output.
