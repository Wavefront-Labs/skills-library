---
id: computing-software.software-engineering.fsharp.global-json-sdk
name: global-json-sdk
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, global-json-sdk, fsharp-project, target-frameworks, rollforward]
level: practitioner
status: docs-checked
description: "Pin the .NET SDK with global.json: version, rollForward policy, allowPrerelease and the lookup rules, for reproducible builds."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/global-json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDK pinning with global.json
**Goal:** the same SDK on every machine.

```json
{
  "sdk": {
    "version": "8.0.100",
    "rollForward": "latestFeature"
  }
}
```
- `global.json` selects the SDK (CLI) version, independent of the runtime a project targets. Create one with `dotnet new globaljson --sdk-version 8.0.302 --roll-forward latestFeature`.
- Lookup: the dotnet muxer starts from the current working directory and searches up through ancestors; the MSBuild project SDK resolver starts from the solution file directory (else the project directory, else the working directory).
- `sdk.version` needs the full version (like 10.0.100); no `10`, `10.0`, `10.0.x`, wildcards or ranges.
- `rollForward` values: `patch`, `feature`, `minor`, `major`, `latestPatch`, `latestFeature`, `latestMinor`, `latestMajor`, `disable`. With a version set and no `rollForward`, the default is `patch` (use the specified version, else the latest patch level, else fail). `disable` requires an exact match. `latestFeature` takes the highest installed feature band and patch with the same major and minor and a value at or above the specified one. `latestMajor` takes the highest installed SDK at or above the specified version. A version must accompany `rollForward` unless it is `latestMajor`.
- With no `global.json`, or none that sets a version or `allowPrerelease`, the highest installed SDK is used.
- `allowPrerelease` (boolean): outside Visual Studio the default is true; in Visual Studio it follows the preview setting.
- .NET 10 SDK adds `paths` (extra SDK search locations, `$host$` for the running dotnet; works only for SDK commands such as `dotnet run`) and `errorMessage`. `msbuild-sdks` pins project SDK versions in one place. Comments are allowed in the file.

## Gotchas
- With package lock files, the page advises `rollForward: disable` so the SDK and dependency graph stay in lockstep.
- Visual Studio installs only one copy of the SDK and removes the previous one on upgrade; install the stand-alone SDK to keep a pinned version.
- An invalid version such as `"10.0"` shows "Version '10.0' is not valid for the 'sdk/version' value." in `dotnet --info`.

## Self-check
Run `dotnet --info` inside the repo with a deliberately invalid version and see the error, then fix it.

## Checked
Checked against the Microsoft Learn "global.json overview" page.
Removed: target framework and F# LangVersion advice, the netstandard note, the "compatible SDK was not found" message and the `dotnet --version` claim (none on the page).
Method: docs-only read of cited pages, 2026-11-08
