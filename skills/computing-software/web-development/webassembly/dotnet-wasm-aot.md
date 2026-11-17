---
id: computing-software.web-development.webassembly.dotnet-wasm-aot
name: dotnet-wasm-aot
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, dotnet-wasm-browser, wasmbuildtools, wasm-aot-dotnet, dotnet-wasm, teavm-java, kotlin-wasm, wasm]
level: practitioner
status: docs-checked
description: ".NET runtime in Wasm"
sources: ["https://raw.githubusercontent.com/dotnet/AspNetCore.Docs/main/aspnetcore/blazor/webassembly-build-tools-and-aot.md", "https://raw.githubusercontent.com/dotnet/runtime/main/src/mono/wasm/features.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .NET on WebAssembly

Goal: build .NET for Wasm.
- The .NET WebAssembly build tools are based on Emscripten. Install with `dotnet workload install wasm-tools` (administrative shell); to target an older release from a newer SDK use `wasm-tools-net{MAJOR VERSION}`, for example `wasm-tools-net8`. Workloads are installed per SDK. On Linux install Python yourself; it is bundled only on Windows and macOS.
- AOT: set `<RunAOTCompilation>true</RunAOTCompilation>` in the project file and `dotnet publish -c Release`. AOT runs only on publish, not in development.
- Without AOT the app runs on an IL interpreter implemented in Wasm. AOT improves runtime speed (CPU-heavy apps benefit most) at the cost of size: the page says most AOT apps are about twice the size of the IL versions.
- Exception handling is on by default from .NET 8; disable with `<WasmEnableExceptionHandling>false</WasmEnableExceptionHandling>`.
- JS interop: annotate `static` C# methods with `[JSImport]` or `[JSExport]`; per the runtime features page this is limited to the main thread even when multi-threading is enabled.
Verify: the AOT build runs faster than the interpreted build on a CPU-bound test.

## Checked

2026-11-08. Confirmed in the ASP.NET Core Blazor build tools and AOT page (read in full) and the dotnet/runtime features page (searched for the `[JSImport]`/`[JSExport]` passages only).
Removed as unconfirmed: the trimming-as-a-setting advice (the page says AOT does not trim managed DLLs) and the `[JSImport]` "confirm per version" caveat.
Method: documentation only; no commands were run.
