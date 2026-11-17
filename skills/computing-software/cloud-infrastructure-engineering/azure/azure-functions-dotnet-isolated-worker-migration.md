---
id: computing-software.cloud-infrastructure-engineering.azure.azure-functions-dotnet-isolated-worker-migration
name: azure-functions-dotnet-isolated-worker-migration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-functions, isolated-worker, in-process-migration, dotnet, functions-worker-sdk]
level: practitioner
status: docs-checked
description: "Migrate .NET Azure Functions from the in-process model (support ends Nov 2026) to the isolated worker: packages, Program.cs, attributes, bindings, HTTP and safe rollout."
sources: ["https://learn.microsoft.com/en-us/azure/azure-functions/migrate-dotnet-to-isolated-model", "https://learn.microsoft.com/en-us/azure/azure-functions/dotnet-isolated-process-guide", "https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .NET in-process to isolated worker migration

**Goal:** move every .NET function app to the isolated worker model before in-process support ends
(10 November 2026), without behaviour changes in production.

## Project changes
```xml
<!-- project element: <Project Sdk="Azure.Functions.Sdk/1.0.0"> -->
<PropertyGroup>
  <TargetFramework>net10.0</TargetFramework>
</PropertyGroup>
<ItemGroup>
  <FrameworkReference Include="Microsoft.AspNetCore.App" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker" Version="2.52.0" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore" Version="2.1.0" />
  <PackageReference Include="Microsoft.ApplicationInsights.WorkerService" Version="2.22.0" />
  <PackageReference Include="Microsoft.Azure.Functions.Worker.ApplicationInsights" Version="1.2.0" />
</ItemGroup>
<ItemGroup>
  <Using Include="System.Threading.ExecutionContext" Alias="ExecutionContext"/>
</ItemGroup>
```
The versions above are the ones shown in the migration guide at the check date; take current versions from the guide. Target .NET 10 (or .NET Framework 4.8 if you depend on .NET Framework-only libraries). Remove `Microsoft.NET.Sdk.Functions` and every `Microsoft.Azure.WebJobs.*` package reference - use the `Microsoft.Azure.Functions.Worker.Extensions.*` equivalents listed in each binding's reference page.

## Program.cs
```csharp
var builder = FunctionsApplication.CreateBuilder(args);
builder.ConfigureFunctionsWebApplication();          // ASP.NET Core integration for HTTP
builder.Services.AddApplicationInsightsTelemetryWorkerService();
builder.Services.ConfigureFunctionsApplicationInsights();
builder.Services.AddSingleton<IOrderService, OrderService>();
builder.Build().Run();
```

## Code changes
- `[FunctionName("X")]` -> `[Function("X")]`; `ILogger` via constructor injection (`ILogger<T>`), not a parameter.
- Trigger and binding attributes are renamed in each binding's isolated-model reference; output binding attributes typically get an `Output` suffix (for example `QueueOutput`).
- HTTP: with ASP.NET Core integration (`ConfigureFunctionsWebApplication`) you keep a familiar programming model for HTTP triggers.
- Durable Functions orchestrators use `TaskOrchestrationContext` (for example `CurrentUtcDateTime`) in the isolated worker.
- `local.settings.json` and app setting: `FUNCTIONS_WORKER_RUNTIME=dotnet-isolated`.

## Rollout
1. Migrate in a branch; run integration tests locally with Core Tools v4.
2. Deploy to a **staging slot** with `FUNCTIONS_WORKER_RUNTIME=dotnet-isolated` as a slot-sticky setting change
   plan (or a new app), warm up, swap.
3. Watch App Insights for binding errors and changed log categories.

## Gotchas
- Some binding behaviours differ from in-process; check each binding's reference for the isolated model.
- Flex Consumption does not support the C# in-process model (isolated .NET 8, 9 and 10).

## Verify
- [ ] All functions listed in the portal after deploy; trigger tests pass; no in-process apps remain (`FUNCTIONS_WORKER_RUNTIME=dotnet` audit via ARG/appsettings).

## Checked
Checked 2026-10-24 against azure-docs azure-functions pages (migrate-dotnet-to-isolated-model and its .NET 10 project include, dotnet-isolated-process-guide, flex-consumption-plan). Confirmed: in-process support ends November 10, 2026; Function replaces FunctionName; FUNCTIONS_WORKER_RUNTIME=dotnet-isolated; Azure.Functions.Sdk/1.0.0 project SDK with net10.0 and the package versions shown; services.AddApplicationInsightsTelemetryWorkerService and services.ConfigureFunctionsApplicationInsights; ConfigureFunctionsWebApplication; Output suffix for output bindings; Flex Consumption lacks in-process support. Found stale and fixed: the net8.0 and classic-SDK csproj example (the guide now shows .NET 10 and the Azure.Functions.Sdk project SDK). Removed unconfirmed: IAsyncCollector and HttpResult statements, Microsoft.Extensions.Azure injection, the Durable package name, App Insights Warning default.

Method: documentation only; no commands were run.
