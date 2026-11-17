---
id: computing-software.software-engineering.csharp-dotnet.single-file-readytorun-and-self-contained-publish
name: single-file-readytorun-and-self-contained-publish
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-publish, single-file-publish, readytorun, self-contained-deployment, trimming, runtime-identifier]
level: practitioner
status: docs-checked
description: "Choose .NET publish options: self-contained vs framework-dependent, PublishSingleFile, ReadyToRun, compression, runtime identifiers, and what breaks in single-file apps."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/deploying/single-file/overview", "https://learn.microsoft.com/en-us/dotnet/core/deploying/ready-to-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-file, ReadyToRun and self-contained publish

```bash
dotnet publish -c Release -r linux-x64 --self-contained true \
  -p:PublishSingleFile=true -p:PublishReadyToRun=true -p:EnableCompressionInSingleFile=true
```
```xml
<PropertyGroup>
  <RuntimeIdentifier>linux-x64</RuntimeIdentifier>   <!-- also sets SelfContained to true by default -->
  <PublishSingleFile>true</PublishSingleFile>
  <PublishReadyToRun>true</PublishReadyToRun>
</PropertyGroup>
```

## Single-file
- Available for both framework-dependent and self-contained apps. A self-contained single file is large because it includes the runtime and framework libraries; the option can be combined with ReadyToRun and trimming.
- Only managed DLLs are bundled. Native runtime binaries stay separate files unless `IncludeNativeLibrariesForSelfExtract` is true (they are then extracted at start). `IncludeAllContentForSelfExtract` extracts everything and is a not-recommended .NET Core 3.1 compatibility mode.
- Extraction directory: `DOTNET_BUNDLE_EXTRACT_BASE_DIR` if set; otherwise a directory under `$HOME/.net` on Linux/macOS or `%TEMP%/.net` on Windows. Keep it unwritable by other privilege levels, and do not use `/tmp`. Under systemd `$HOME` may be undefined, so set `DOTNET_BUNDLE_EXTRACT_BASE_DIR` explicitly.
- Keep a file outside the bundle with `<ExcludeFromSingleFile>true</ExcludeFromSingleFile>` metadata plus `CopyToPublishDirectory`.
- `EnableCompressionInSingleFile=true` compresses embedded assemblies; they are decompressed into memory at start, so measure both size and startup cost.
- PDBs sit beside the app, not in the bundle; set `<DebugType>embedded</DebugType>` on a project to embed its PDB in the assembly.
- APIs that break: `Assembly.Location` returns an empty string; `Assembly.CodeBase`/`EscapedCodeBase` throw `PlatformNotSupportedException`; `Assembly.GetFile(s)` throw `IOException`; `AssemblyName.CodeBase` returns null. Use `AppContext.BaseDirectory` to find files next to the executable.
- IIS does not support single-file apps with the in-process hosting model. Managed C++ components are not well suited to single-file.
- Signing: the SDK provides MSBuild extension points to process binaries just before bundling.

## ReadyToRun
- A form of ahead-of-time compilation that improves startup and first-use latency; enable with `PublishReadyToRun` (the docs' example publishes with `-r win-x64`).
- AOT code is less optimised than JIT output, so tiered compilation replaces commonly used ReadyToRun methods with JIT-generated ones. R2R does not prevent the JIT from running.
- For self-contained apps the framework assemblies are precompiled too. Exclude assemblies with `PublishReadyToRunExclude`; C++/CLI binaries are not eligible. `PublishReadyToRunEmitSymbols` emits symbols for profilers.
- Composite ReadyToRun (`PublishReadyToRunComposite`) was self-contained-only in .NET 6.
- Cross-compilation: for .NET 6 and later a Windows x64 SDK can target Windows, Linux and macOS; a Linux x64 SDK can target Linux and macOS (see the page's table for each SDK platform).

## Verify
Run the published binary on a clean machine or container without the SDK; compare startup against a plain build.

## Checked
2026-11-08. Confirmed against the Single-file deployment overview (availability, native library bundling and extraction rules, environment variable, ExcludeFromSingleFile, DebugType embedded, compression, API incompatibility table, IIS note, signing extension points) and the ReadyToRun page (PublishReadyToRun, tiered compilation interaction, exclusion, composite note, cross-compilation table). The "Deploying .NET apps" overview was not used. Removed as unconfirmed: size and speed figures, the InvariantGlobalization comment, the trimming rules and IL2026/IL3050 advice, the container image advice, signing-after-bundle and antivirus remarks, and the RID-less ReadyToRun error.
Method: documentation only; no commands were run.
