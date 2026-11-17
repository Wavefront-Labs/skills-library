---
id: computing-software.software-engineering.fsharp.readytorun-single-file
name: readytorun-single-file
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, readytorun-single-file, fsharp-aot, ready-to-run, single-file-publish]
level: practitioner
status: docs-checked
description: "Speed up .NET startup and simplify deployment with ReadyToRun and single-file publishing, with the documented size, extraction and API caveats."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/deploying/ready-to-run
  - https://learn.microsoft.com/en-us/dotnet/core/deploying/single-file/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReadyToRun and single-file
**Goal:** faster start and one-file deploys.

```bash
dotnet publish -c Release -r win-x64 --self-contained true \
  -p:PublishReadyToRun=true -p:PublishSingleFile=true
dotnet publish -r linux-x64 --self-contained false -p:PublishSingleFile=true
```
- `PublishReadyToRun=true` compiles assemblies to R2R, a form of ahead-of-time compilation that reduces JIT work at startup and on first use of code. It only works when publishing for a specific RID. R2R binaries hold both IL and native code, typically two to three times larger. Apps with little code will likely see no significant gain.
- Tiered compilation replaces commonly used R2R methods with JIT-generated ones; R2R does not stop the JIT running (generics from other assemblies, native interop, hardware intrinsics, dynamic methods and unusual IL can still need it).
- Exclude assemblies with `<PublishReadyToRunExclude Include="X.dll" />`; `PublishReadyToRunEmitSymbols` emits profiler symbols (.ni.pdb on Windows, .r2rmap on Linux); `PublishReadyToRunComposite` (.NET 6+) compiles assemblies together for better optimisation but slower compile and much bigger output, recommended only with tiered compilation disabled or Linux self-contained for best startup.
- `PublishSingleFile` bundles the app into one file, for both framework-dependent and self-contained apps, and can combine with R2R and trimming. `RuntimeIdentifier` also defaults `SelfContained` to true. Single-file apps are OS and architecture specific. `*.runtimeconfig.json` and `*.deps.json` are included in the file.
- Set `PublishSingleFile` in the project file to get single-file compatibility warnings at build time.
- Only managed DLLs are bundled; the runtime's native binaries stay separate unless `IncludeNativeLibrariesForSelfExtract` is true. `EnableCompressionInSingleFile` compresses embedded assemblies at a start-up cost, so measure both. `ExcludeFromSingleFile` metadata leaves a file loose; `DebugType` embedded puts the PDB in the assembly.

## Gotchas
- When extraction is used, files go under `DOTNET_BUNDLE_EXTRACT_BASE_DIR`, else `$HOME/.net` on Linux and macOS or `%TEMP%/.net` on Windows. Keep that directory unwritable by other privilege levels; under systemd `$HOME` may be undefined, so set the variable (the page suggests `%h/.net`).
- `Assembly.Location` returns an empty string and `Assembly.CodeBase` throws PlatformNotSupportedException. Use `AppContext.BaseDirectory` for files next to the executable and `Environment.ProcessPath` for the executable path.
- IIS in-process hosting of ASP.NET Core does not support single-file apps.

## Self-check
Publish a small console app both ways and confirm the single-file output has no loose managed DLLs.

## Checked
Checked against the Microsoft Learn "ReadyToRun Compilation" and "Single-file deployment" pages.
Removed: the claim that reflection still works under R2R, the F# trimming-risk line, the "R2R is per-RID" wording kept only as the RID requirement, the `time` self-check and the generic index source.
Method: docs-only read of cited pages, 2026-11-08
