---
id: computing-software.software-engineering.csharp-dotnet.aspnet-core-health-checks-and-graceful-shutdown
name: aspnet-core-health-checks-and-graceful-shutdown
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, aspnet-core, aspnet-health-checks, graceful-shutdown, kubernetes-probes, ihostedservice]
level: practitioner
status: docs-checked
description: "Expose liveness and readiness health checks in ASP.NET Core, wire them to Kubernetes probes, and shut down gracefully with host timeouts and IHostApplicationLifetime."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host
  - https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.hostoptions.shutdowntimeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASP.NET Core health checks and graceful shutdown

**Goal:** the orchestrator routes traffic only to ready instances, restarts only truly broken ones, and deployments drop no requests.

## 1. Register checks with tags
```csharp
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy(), tags: ["live"])
    .AddCheck<QueueBacklogCheck>("queue", failureStatus: HealthStatus.Degraded, tags: ["ready"]);

app.MapHealthChecks("/healthz/live",  new() { Predicate = r => r.Tags.Contains("live") });
app.MapHealthChecks("/healthz/ready", new() { Predicate = r => r.Tags.Contains("ready") });
```
- **Liveness**: is the process able to make progress? No dependency checks; a DB outage must not restart every pod.
- **Readiness**: can it serve traffic now? Dependencies, warm-up done.
- Startup probe for slow boots instead of a long liveness `initialDelaySeconds`.

## 2. Custom check
```csharp
public sealed class QueueBacklogCheck(IQueueStats stats) : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext ctx, CancellationToken ct = default)
    {
        var depth = await stats.DepthAsync(ct);
        return depth < 10_000 ? HealthCheckResult.Healthy() : HealthCheckResult.Degraded($"backlog {depth}");
    }
}
```
Keep checks fast (`AddCheck<T>` accepts an optional `timeout`); probes hit them every few seconds. Expose details (JSON writer) only on an internal port or behind `RequireAuthorization()` (the health checks docs describe both).

## 3. Kubernetes wiring
```yaml
livenessProbe:  { httpGet: { path: /healthz/live,  port: 8080 }, periodSeconds: 10, failureThreshold: 3 }
readinessProbe: { httpGet: { path: /healthz/ready, port: 8080 }, periodSeconds: 5 }
terminationGracePeriodSeconds: 40
```

## 4. Graceful shutdown
On SIGTERM the host: signals `ApplicationStopping`, stops accepting connections (Kestrel), waits for in-flight requests, stops hosted services, all within `HostOptions.ShutdownTimeout` (default 30 s in the current runtime source; it can also be set with the `shutdownTimeoutSeconds` host setting).
```csharp
builder.Services.Configure<HostOptions>(o => o.ShutdownTimeout = TimeSpan.FromSeconds(30));
```
Background services must honour the token:
```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    while (!stoppingToken.IsCancellationRequested)
        await ProcessBatchAsync(stoppingToken);
}
```
Endpoint removal and SIGTERM are not synchronised in Kubernetes, so traffic can still arrive after SIGTERM; a `preStop` delay or failing readiness on `ApplicationStopping` reduces connection errors.

## Gotchas
- `ShutdownTimeout` must be shorter than `terminationGracePeriodSeconds`, or SIGKILL interrupts cleanup.
- An exception escaping `ExecuteAsync` stops the host by default (`HostOptions.BackgroundServiceExceptionBehavior` defaults to `StopHost`); catch and log per iteration.

## Verify
- `kubectl rollout restart` under a load test shows zero 5xx/connection errors, and stopping the database flips readiness to 503 without restarting pods.

## Checked

Checked 2026-10-25 against aspnet/AspNetCore.Docs (host-and-deploy/health-checks), dotnet/docs (generic-host), dotnet/dotnet-api-docs (HostOptions, AddCheck) and dotnet/runtime `HostOptions.cs` on main.
Confirmed: `ShutdownTimeout` default 30 s and the `shutdownTimeoutSeconds` setting; `BackgroundServiceExceptionBehavior` default `StopHost`; `AddCheck` has an optional `timeout` parameter; `RequireAuthorization` on health endpoints; tags and `Predicate` filtering; separate readiness and liveness probes with a Kubernetes example.
Removed as unconfirmed: third-party NpgSql/Redis check packages, the version history of the default timeout, the `.AllowAnonymous()` fallback-policy gotcha.

Method: documentation only; no commands were run.
