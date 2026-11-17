---
id: computing-software.software-engineering.csharp-dotnet.sdk-pinning-with-global-json
name: sdk-pinning-with-global-json
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-cli, global-json, sdk-version, rollforward, msbuild-sdks, dotnet-sdk-cli]
level: practitioner
status: docs-checked
description: "Pin the .NET SDK with global.json: version and rollForward policies, CI setup, side-by-side SDKs, MSBuild SDK versions and diagnosing 'SDK not found' errors."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/tools/global-json
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script
  - https://github.com/actions/setup-dotnet
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SDK pinning with global.json

**Goal:** every developer and CI agent builds with the same SDK band, so new compiler warnings, analyzers and MSBuild behaviour arrive by explicit upgrade.

## 1. The file
```json
{
  "sdk": {
    "version": "9.0.100",
    "rollForward": "latestFeature",
    "allowPrerelease": false
  }
}
```
```bash
dotnet new globaljson --sdk-version 9.0.100 --roll-forward latestFeature
dotnet --version          # SDK actually selected in this directory
dotnet --list-sdks
```
The `dotnet` CLI searches for `global.json` from the current working directory upward, and the MSBuild SDK resolver starts from the solution or project directory; put `global.json` at the repo root.

## 2. rollForward policies
| Policy | Behaviour (requested 9.0.100) |
|---|---|
| `patch` (default when a version is given) | specified version, else latest patch of that band, else fail |
| `latestPatch` | highest installed patch in the same band, at or above the requested one |
| `feature` | latest patch of the band; else next higher feature band in the same major.minor |
| `latestFeature` | highest installed feature band and patch in the same major.minor |
| `minor` / `latestMinor` | as above, and may move to a higher minor in the same major |
| `major` / `latestMajor` | may move to any higher major |
| `disable` | exact match required |
`latestFeature` is a reasonable choice when you want patches and feature bands applied but major/minor upgrades deliberate. The docs recommend `disable` when you use package lock files, so the SDK and dependency graph stay in lockstep.

## 3. SDK vs runtime
The SDK version (9.0.100) selects the SDK that builds the project; `TargetFramework` (for example net8.0) selects the target runtime API surface. A newer SDK can build older targets.

## 4. CI
```yaml
- uses: actions/setup-dotnet@v6
  with:
    global-json-file: global.json
```
Without a pinned version, setup-dotnet's docs warn that the latest version installed on the runner is used. `dotnet-install` also accepts a `global.json` through its `-JSonFile` option (`--jsonfile` in the shell script).

## 5. Errors
- If the requested SDK is not installed and `rollForward` does not allow another one, the SDK resolver reports that no compatible SDK was found: install it or relax `rollForward`.
- `dotnet --info` shows the global.json in use and the installed SDKs.

## Gotchas
- Because the search walks up the directory tree, a `global.json` in a parent folder applies to every repo below it.
- `allowPrerelease` defaults to `true` outside Visual Studio when not set; set it to `false` explicitly if you do not want prerelease SDKs.
- A `global.json` can also carry `msbuild-sdks`, and from the .NET 10 SDK `paths` and `errorMessage`.

## Verify
- `dotnet --version` in the repo matches the pinned SDK on dev machines and CI logs, and upgrading means a one-line PR that CI validates.

## Checked

Checked 2026-10-25 against dotnet/docs (core/tools/global-json, dotnet-install-script), actions/setup-dotnet README and advanced-usage on main.
Confirmed: `dotnet new globaljson --sdk-version --roll-forward`; rollForward values and behaviours; `patch` default when a version is given; `allowPrerelease` default is `true` outside Visual Studio (the earlier "defaults to false since SDK 6" was wrong); `msbuild-sdks`, `paths` and `errorMessage` (.NET 10 SDK); search starts at the working directory (CLI) or the solution/project directory (MSBuild resolver) and walks up; `rollForward: disable` recommended with lock files; `global-json-file` input of setup-dotnet; `-JSonFile` for dotnet-install.
Removed as unconfirmed: the Traversal SDK version, the Docker tag advice, the x64/arm64 and snap/apt causes, the Visual Studio resolution note, the feature-band explanation.

Method: documentation only; no commands were run.
