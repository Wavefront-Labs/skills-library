---
id: computing-software.software-engineering.csharp-dotnet.dotnet-aspire-app-host
name: dotnet-aspire-app-host
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-hosting, aspire-app-host, dotnet-aspire, service-discovery, service-defaults, opentelemetry]
level: practitioner
status: draft
description: "Compose distributed .NET apps with Aspire: AppHost resources, WithReference service discovery, ServiceDefaults telemetry, integrations, local dashboard and manifest-based deployment."
sources: ["https://learn.microsoft.com/en-us/dotnet/aspire/get-started/aspire-overview", "https://learn.microsoft.com/en-us/dotnet/aspire/fundamentals/app-host-overview", "https://learn.microsoft.com/en-us/dotnet/aspire/service-discovery/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aspire AppHost

Aspire (9.x on .NET 8/9) gives a code-first model of your app: services, containers and cloud resources, wired together for local dev with a dashboard (logs, traces, metrics) and exportable to deployment targets.

```csharp
// MyApp.AppHost/Program.cs   (templates: dotnet new aspire-starter; dotnet new install Aspire.ProjectTemplates)
var builder = DistributedApplication.CreateBuilder(args);

var cache = builder.AddRedis("cache");
var pg    = builder.AddPostgres("pg").WithDataVolume().AddDatabase("catalogdb");
var api   = builder.AddProject<Projects.CatalogApi>("api")
                   .WithReference(pg).WithReference(cache)      // injects connection strings and service-discovery info
                   .WaitFor(pg)                                  // start ordering
                   .WithReplicas(2);
builder.AddProject<Projects.Web>("web").WithExternalHttpEndpoints().WithReference(api);
builder.Build().Run();
```
```csharp
// each service: references ServiceDefaults project
builder.AddServiceDefaults();                   // OpenTelemetry, health checks, service discovery, HttpClient resilience
builder.AddNpgsqlDbContext<CatalogDb>("catalogdb");   // client integration reads ConnectionStrings:catalogdb
var client = new HttpClient { BaseAddress = new("https+http://api") };   // resolved by service discovery
```
## Concepts
- AppHost is orchestration for dev (and a model for deployment); it is not a production runtime. Deploy with `azd` (Azure Container Apps), Kubernetes manifests via Aspirate/publishers, or Docker Compose publishers.
- Resources: projects, containers (`AddContainer`), executables, parameters (`AddParameter(secret: true)`), cloud (Azure Service Bus, Storage).
- Hosting packages (`Aspire.Hosting.*`) live in the AppHost only; client integration packages (`Aspire.Npgsql...`) live in services.
- Docker (or Podman) is required for container resources.
- Dashboard shows structured logs, distributed traces and metrics through OTLP.

## Gotchas
- `WithReference` order vs `WaitFor`: reference does not wait; add `WaitFor`.
- Connection string names must match resource names.
- Secrets: parameters resolve from user secrets locally; do not hard-code.
- Persistent data needs `WithDataVolume`/bind mount; containers are otherwise recreated.
- Version drift between AppHost SDK and packages causes build errors; update together.

## Verify
`dotnet run --project MyApp.AppHost` opens the dashboard; all resources show Running; a trace spans web -> api -> db.
