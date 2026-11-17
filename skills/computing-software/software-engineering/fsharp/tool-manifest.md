---
id: computing-software.software-engineering.fsharp.tool-manifest
name: tool-manifest
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, tool-manifest, fsharp-ci, dotnet-tool-manifest, local-tools]
level: practitioner
status: draft
description: "Pin developer tools (Fantomas, Paket, FAKE, fsdocs) per repository using .config/dotnet-tools.json."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local tools
**Goal:** every contributor and CI uses the same tool versions.

```bash
dotnet new tool-manifest
dotnet tool install fantomas
dotnet tool install paket
dotnet tool install fake-cli
dotnet tool restore
dotnet tool list
dotnet tool update fantomas
```
- The manifest lives at `.config/dotnet-tools.json`; commit it.
- Run tools with `dotnet <toolname>` (for example `dotnet fantomas`); the command name comes from the package.
- Global tools (`-g`) are per user and not pinned; avoid them in CI.
- `dotnet tool restore` is the first CI step after checkout.

## Gotchas
- Tools need a compatible runtime; a tool targeting an older runtime may need `DOTNET_ROLL_FORWARD` or a newer SDK.
- Tool package IDs differ from command names (`fake-cli` provides `dotnet fake`).

## Self-check
Fresh clone, `dotnet tool restore`, then `dotnet fantomas --version` works.
