---
id: computing-software.software-engineering.fsharp.secrets-configuration
name: secrets-configuration
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, secrets-configuration, fsharp-security, user-secrets, iconfiguration]
level: practitioner
status: draft
description: "Keep secrets out of source using user-secrets, environment variables and IConfiguration binding in F#."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration and secrets
**Goal:** no credentials in the repo.

```bash
dotnet user-secrets init --project src/App
dotnet user-secrets set "Db:ConnectionString" "Server=...;..." --project src/App
```
```fsharp
open Microsoft.Extensions.Configuration

let config =
    ConfigurationBuilder()
        .AddJsonFile("appsettings.json", optional = true)
        .AddEnvironmentVariables()
        .AddUserSecrets<Marker>()          // Marker: any type in the assembly
        .Build()

let conn = config.["Db:ConnectionString"]
```
- Environment variables use `__` for nesting (`Db__ConnectionString`).
- User secrets are for development only and stored outside the repo; production uses the platform secret store (Key Vault, Kubernetes secrets, etc.).
- Later providers override earlier ones; order the builder accordingly.
- Bind sections to records with `config.GetSection("Db").Get<DbOptions>()` (needs `[<CLIMutable>]` records and the Binder package).

## Gotchas
- Logging configuration objects can leak secrets; redact.
- `appsettings.*.json` committed with real values is the usual leak.

## Self-check
`dotnet user-secrets list` shows the key and `git status` shows no changes.
