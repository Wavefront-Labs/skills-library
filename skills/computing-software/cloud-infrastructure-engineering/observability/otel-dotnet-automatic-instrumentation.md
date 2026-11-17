---
id: computing-software.cloud-infrastructure-engineering.observability.otel-dotnet-automatic-instrumentation
name: otel-dotnet-automatic-instrumentation
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [dotnet-auto-instrumentation-setup, otel-dotnet-auto, language-instrumentation, zero-code-instrumentation, dotnet]
level: practitioner
status: docs-checked
description: "Install OpenTelemetry .NET automatic instrumentation: install script, profiler and startup-hook env vars, IIS and Windows services, NuGet package mode, and enabling sources."
sources: ["https://opentelemetry.io/docs/zero-code/dotnet/", "https://opentelemetry.io/docs/zero-code/dotnet/configuration/", "https://github.com/open-telemetry/opentelemetry-dotnet-instrumentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .NET automatic instrumentation

Uses a CLR profiler + startup hook to inject the OTel .NET SDK and instrumentations into unmodified apps (.NET Framework
4.6.2 is the minimum supported version).

## Linux/macOS
```bash
curl -sSfL https://github.com/open-telemetry/opentelemetry-dotnet-instrumentation/releases/latest/download/otel-dotnet-auto-install.sh -O
sh ./otel-dotnet-auto-install.sh                     # installs to $HOME/.otel-dotnet-auto (OTEL_DOTNET_AUTO_HOME)
chmod +x $HOME/.otel-dotnet-auto/instrument.sh
. $HOME/.otel-dotnet-auto/instrument.sh              # exports CORECLR_* and DOTNET_STARTUP_HOOKS etc.
OTEL_SERVICE_NAME=billing OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-agent:4318 dotnet Billing.dll
```
The env vars set: `CORECLR_ENABLE_PROFILING=1`, `CORECLR_PROFILER={918728DD-259F-4A6A-AC2B-B85E1B658318}`,
`CORECLR_PROFILER_PATH`, `DOTNET_ADDITIONAL_DEPS`, `DOTNET_SHARED_STORE`, `DOTNET_STARTUP_HOOKS`, `OTEL_DOTNET_AUTO_HOME`.
In containers, copy the install dir into the image and set these explicitly.

## Windows / IIS
```powershell
Import-Module "OpenTelemetry.DotNet.Auto.psm1"
Install-OpenTelemetryCore
Register-OpenTelemetryForIIS                         # restarts IIS
Register-OpenTelemetryForWindowsService -WindowsServiceName "BillingSvc" -OTelServiceName "billing"
```
For .NET Framework apps, common `OTEL_` settings can go in `appSettings` in App.config.

## NuGet package mode
The docs describe installing via the `OpenTelemetry.AutoInstrumentation` NuGet packages; see "Using the OpenTelemetry.AutoInstrumentation NuGet packages" on the .NET zero-code page.

## Configuration
- Disable one: `OTEL_DOTNET_AUTO_TRACES_{INSTRUMENTATION_ID}_INSTRUMENTATION_ENABLED=false` (ids are in the docs' instrumentation table).
- Disable all of a signal: `OTEL_DOTNET_AUTO_TRACES_INSTRUMENTATION_ENABLED=false`, then enable specific ones with the per-id variable.
- Your own ActivitySources/Meters: `OTEL_DOTNET_AUTO_TRACES_ADDITIONAL_SOURCES=Acme.*`,
  `OTEL_DOTNET_AUTO_METRICS_ADDITIONAL_SOURCES=Acme.*`.
- Diagnostics: `OTEL_DOTNET_AUTO_LOG_DIRECTORY`, `OTEL_LOG_LEVEL=debug`.

## Gotchas
- `DOTNET_ADDITIONAL_DEPS` and `DOTNET_SHARED_STORE` are used to mitigate assembly version conflicts.
- On .NET 8 and later, `DOTNET_EnableDiagnostics=0` disables all diagnostics, including the CLR profiler facility the agent needs.
- On .NET 8 and higher the app must reference `Grpc.Net.Client` to use the gRPC OTLP exporter protocol.

## Checked
- 2026-10-28. Checked against the OpenTelemetry .NET zero-code pages (index, configuration) and the opentelemetry-dotnet-instrumentation README (main, 2026-10).
- Confirmed: install script and `instrument.sh`, profiler variables and CLSID, `DOTNET_ADDITIONAL_DEPS`, `DOTNET_SHARED_STORE`, IIS and Windows service cmdlets and parameters, `OTEL_DOTNET_AUTO_TRACES_ADDITIONAL_SOURCES`, `OTEL_DOTNET_AUTO_METRICS_ADDITIONAL_SOURCES`, `OTEL_DOTNET_AUTO_LOG_DIRECTORY`, .NET Framework 4.6.2 minimum.
- Fixed: per-instrumentation variable now uses the documented `{INSTRUMENTATION_ID}` pattern. Removed (unconfirmed): .NET 8+ as a support floor, appcmd/web.config advice, "only one profiler", trimmed-app claim, `dotnet add package` flow.
Method: documentation only; no commands were run.
