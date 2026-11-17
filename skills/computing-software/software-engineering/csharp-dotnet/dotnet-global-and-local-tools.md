---
id: computing-software.software-engineering.csharp-dotnet.dotnet-global-and-local-tools
name: dotnet-global-and-local-tools
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-tools, tool-manifest, dotnet-tool-restore, dnx, packing-tools, dotnet-cli]
level: practitioner
status: docs-checked
description: "Install and pin .NET CLI tools: local tool manifests restored in CI, global and tool-path installs, one-shot dnx/dotnet tool exec, and packaging your own tool."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools
  - https://learn.microsoft.com/en-us/dotnet/core/tools/local-tools-how-to-use
  - https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools-how-to-create
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-exec
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .NET global and local tools

**Goal:** every developer and CI agent runs the same versions of dotnet-ef, csharpier,
reportgenerator and friends, without machine-wide installs.

## Local tools (per repo, preferred)
```bash
dotnet new tool-manifest                       # creates .config/dotnet-tools.json
dotnet tool install dotnet-ef --version <version>
dotnet tool restore                            # CI and fresh clones: installs manifest versions
dotnet ef migrations add Init                  # or: dotnet tool run dotnet-ef ...
```
Commit `.config/dotnet-tools.json`. The tools in a manifest are available to the directory containing `.config` and its subdirectories. Update with `dotnet tool update <id>`; list with `dotnet tool list`.

## Global tools (per user)
```bash
dotnet tool install -g dotnet-counters
dotnet tool update -g dotnet-counters
dotnet tool list -g
```
Installed to `$HOME/.dotnet/tools` on Linux/macOS and `%USERPROFILE%\.dotnet\tools` on Windows (a default directory added to PATH). Fine for personal diagnostics tools; not for
build steps others depend on.

## Tool path (containers, CI images)
```bash
dotnet tool install dotnet-trace --tool-path /tools
/tools/dotnet-trace collect -p 1
```
Tool-path tools are invoked from the installation directory or by adding that directory to PATH.

## One-shot execution
With the .NET 10 SDK, `dnx <tool>` (and `dotnet tool exec`) runs a tool package without installing it, for example `dnx dotnet-counters monitor --process-id <pid>`.

## Creating a tool
```xml
<PropertyGroup>
  <OutputType>Exe</OutputType>
  <TargetFramework>net8.0</TargetFramework>
  <PackAsTool>true</PackAsTool>
  <ToolCommandName>acme-lint</ToolCommandName>
  <PackageId>Acme.Lint</PackageId>
</PropertyGroup>
```
`dotnet pack` then install from the local package folder (`dotnet tool install --global --add-source ./nupkg Acme.Lint`) to test.
Publish to NuGet or an internal feed.

## Gotchas
- A tool from the manifest is missing in CI: add a `dotnet tool restore` step.
- Tools target a framework; without the matching runtime they fail to run.

## Verify
- [ ] Repo has a tool manifest; CI runs `dotnet tool restore` before tool usage.
- [ ] No build scripts depend on globally installed tools.

## Checked

Checked 2026-10-25 against dotnet/docs (core/tools/global-tools, local-tools-how-to-use, global-tools-how-to-create, dotnet-tool-exec) on main.
Confirmed: `dotnet new tool-manifest` and `.config/dotnet-tools.json`; manifest scope (its directory and subdirectories); `dotnet tool restore`; default global tool directories; `--tool-path`; `dnx` needs the .NET 10 SDK and `dotnet tool exec` exists; `PackAsTool`, `ToolCommandName`, `PackageId`; `dotnet pack`.
Removed as unconfirmed: `RollForward` advice, version pins in examples, the CI error message text, private feed advice.

Method: documentation only; no commands were run.
