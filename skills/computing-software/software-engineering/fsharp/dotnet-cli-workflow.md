---
id: computing-software.software-engineering.fsharp.dotnet-cli-workflow
name: dotnet-cli-workflow
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, dotnet-cli-workflow, fsharp-project, dotnet-new, dotnet-watch]
level: intro
status: docs-checked
description: "Drive the F# inner loop with the dotnet CLI: new -lang F#, run, watch, publish and list package, with implicit restore and argument forwarding."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-watch
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dotnet CLI workflow
**Goal:** know the commands used daily.

```bash
dotnet new console --language "F#" -o MyApp
dotnet run --project MyApp -- --flag value
dotnet watch run --project MyApp
dotnet publish MyApp -c Release -o out
dotnet list package --outdated
```
- `dotnet new <template>`: `-lang|--language` takes C#, F# or VB; quote `"F#"` because some shells treat `#` specially. `-o` sets the output directory, `-n` the name (default: the current directory name), `--dry-run` previews, `--force` overwrites existing files, `dotnet new list` lists installed templates.
- Restore runs implicitly in new, build, run, test, publish and pack; disable it with `--no-restore`. An explicit `dotnet restore` still suits CI.
- `dotnet run` builds then runs from the project; with multiple target frameworks it errors unless `-f|--framework` is given. Arguments after `--` go to the application. Output lands in `bin/<configuration>/<target>`. It resolves dependencies from the NuGet cache, so the page says not to use it in production; deploy `dotnet publish` output instead. To run a built DLL use `dotnet myapp.dll`. Launch profiles come from `Properties/launchSettings.json` (`--launch-profile`, `--no-launch-profile`).
- `dotnet watch [run|build|test]` (build and test choices from .NET 8 SDK; default `run`) reruns on file change, hot reloading when the change is supported and restarting otherwise; `--no-hot-reload` turns hot reload off, Ctrl+R forces a rebuild and restart, `--project` picks the project, `--` forwards arguments to the child command. It watches Compile and EmbeddedResource items plus referenced projects, and .config and .json files do not trigger a restart. `DOTNET_USE_POLLING_FILE_WATCHER=1` is needed on network shares and Docker mounted volumes.
- `dotnet publish` output: IL dll, `.deps.json`, `.runtimeconfig.json` and dependencies; `-c` maps to `Configuration` and `-o` to `PublishDir`. With the .NET 8 SDK and net8.0 or later, publish defaults to Release. `-p:PublishProfile=Name` uses `Properties/PublishProfiles/Name.pubxml`.
- `dotnet list package` takes `--outdated`, `--deprecated`, `--vulnerable`, `--include-transitive` and `--format json`; the .NET 10 noun-first form is `dotnet package list`.

## Gotchas
- `dotnet watch` hot reload support for F# was not stated on the page; it points to a separate supported-frameworks list. Check that list before relying on it.
- A rude edit (a change that cannot be hot reloaded) prompts to restart; `--non-interactive` restarts without prompting.

## Self-check
`dotnet new console --language "F#" -o T` then `dotnet run --project T` builds and runs the template program.

## Checked
Checked against the Microsoft Learn reference pages for dotnet new, run, watch, publish and list package.
Removed: `dotnet sln`, `add package`, `add reference`, `test` and `fsi` lines, `dotnet --info`/`--list-sdks`, the MSBuild `-m` gotcha and the "Debug unless -c Release" claim (not on the pages read) and the F# hot reload guess.
Method: docs-only read of cited pages, 2026-11-08
