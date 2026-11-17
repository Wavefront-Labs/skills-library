---
id: computing-software.software-engineering.csharp-dotnet.trimming-and-native-aot
name: trimming-and-native-aot
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, dotnet-cli, native-aot, trimming, publish-trimmed, reflection, startup-performance]
level: practitioner
status: docs-checked
description: "Publish trimmed and Native AOT .NET apps: enabling, reading trim/AOT warnings, source generators instead of reflection, ASP.NET Core AOT limits and size/startup verification."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
  - https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trim-self-contained
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot
  - https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trimming and Native AOT

**Goal:** small, fast-starting self-contained binaries (CLIs, functions, containers) without runtime surprises from removed code.

## 1. Enable
```xml
<PropertyGroup>
  <PublishAot>true</PublishAot>             <!-- Native AOT implies trimming; or PublishTrimmed for JIT + trimming -->
  <InvariantGlobalization>true</InvariantGlobalization>   <!-- drop ICU if culture data not needed -->
  <OptimizationPreference>Size</OptimizationPreference>
  <StackTraceSupport>true</StackTraceSupport>   <!-- false removes stack trace generation support (.NET 8+) -->
</PropertyGroup>
```
```bash
dotnet publish -c Release -r linux-x64      # AOT needs the platform's native toolchain (for example clang on Linux); cross-OS compilation is not supported
```
Setting `PublishAot` also enables dynamic code-usage analysis during build and editing, so warnings appear early. Cross-architecture builds (x64 and arm64) are possible when the native toolchain is installed.

## 2. Treat warnings as bugs
- `IL2026` RequiresUnreferencedCode: API uses reflection the trimmer cannot analyse.
- `IL3050` RequiresDynamicCode: needs runtime code generation (e.g. `MakeGenericType` with value types, Reflection.Emit).
- `IL2070`-`IL2075`: reflection over a `Type` not annotated with `[DynamicallyAccessedMembers]`.
A warning-free publish is the goal; the trimming docs warn that analysis can miss patterns that then fail at runtime.

## 3. Replace reflection with source generators
```csharp
[JsonSerializable(typeof(Order))]
[JsonSerializable(typeof(List<Order>))]
internal partial class AppJsonContext : JsonSerializerContext { }

builder.Services.ConfigureHttpJsonOptions(o => o.SerializerOptions.TypeInfoResolverChain.Insert(0, AppJsonContext.Default));
```
Also prefer other source-generated APIs where they exist (for example `[LoggerMessage]` and `[GeneratedRegex]`).

## 4. ASP.NET Core with AOT
The `webapiaot` template uses minimal APIs only and `WebApplication.CreateSlimBuilder`. The ASP.NET Core compatibility table lists as supported: CORS, gRPC, health checks, JWT authentication, rate limiting, output caching and static files; partial: minimal APIs and SignalR; not supported: MVC, Blazor Server, OData, Session and "other authentication". Check the table for the features you use, including your data-access library.

## 5. Library authors
`<IsAotCompatible>true</IsAotCompatible>` defaults `IsTrimmable`, `EnableTrimAnalyzer`, `EnableSingleFileAnalyzer` and `EnableAotAnalyzer` to true; annotate APIs with `[RequiresUnreferencedCode]` / `[DynamicallyAccessedMembers]` so warnings point at the caller's real problem.

## Gotchas
- Code that depends on runtime code generation or unanalysable reflection (see `IL3050` and `IL2026`) cannot work reliably under AOT.
- Suppressing a trim warning without justification can hide members removed by the trimmer.
- AOT binaries are per RID, and cross-OS compilation is not supported, so build each target OS on that OS in CI.
- Diagnostics differ: Native AOT supports EventPipe since .NET 8 but shares only some diagnostics capabilities with the full runtime.

## Verify
- `dotnet publish` emits zero IL2xxx/IL3xxx warnings, integration tests run against the published binary (not `dotnet run`), and startup time/size are measured against the JIT build.

## Checked

Checked 2026-10-25 against dotnet/docs (core/deploying/native-aot: index, cross-compile, optimizing, diagnostics; trimming: trim-self-contained, trimming-options, trim-warnings) and aspnet/AspNetCore.Docs (fundamentals/native-aot) on main.
Confirmed: `PublishAot`, `PublishTrimmed`, `InvariantGlobalization`, `OptimizationPreference` and `StackTraceSupport` (.NET 8+); `PublishAot` enables build-time analysis; `-r <RID>` publish; native toolchain required; cross-OS AOT unsupported and cross-architecture limited; `IsAotCompatible` default properties; warning pages IL2026, IL2070, IL2075, IL3050 exist; `webapiaot` template, `CreateSlimBuilder`, minimal APIs only; compatibility table entries; `TypeInfoResolverChain.Insert(0, ...)`; EventPipe supported on Native AOT since .NET 8.
Removed as unconfirmed: the `EnableConfigurationBindingGenerator` and request delegate generator remarks, EF Core and Dapper AOT notes, `TreatWarningsAsErrors` advice, symbol file names, specific plugin/ORM examples.

Method: documentation only; no commands were run.
