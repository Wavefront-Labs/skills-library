---
id: computing-software.software-engineering.csharp-dotnet.background-jobs-quartz-hangfire-and-redis
name: background-jobs-quartz-hangfire-and-redis
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-messaging-jobs, quartz-hangfire, stackexchange-redis, quartz, hangfire, job-scheduling]
level: practitioner
status: draft
description: "Schedule and run durable background work in .NET with Quartz.NET and Hangfire (persistent stores, clustering, retries, idempotency) and use StackExchange.Redis for locks, caching and queues."
sources: ["https://www.quartz-scheduler.net/documentation/", "https://docs.hangfire.io/en/latest/", "https://stackexchange.github.io/StackExchange.Redis/Basics"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quartz.NET, Hangfire and Redis

## Choosing
- `BackgroundService` + `PeriodicTimer`: simple in-process loops; lost on restart; every replica runs it.
- **Quartz.NET**: cron/calendar scheduling, job data, misfire policies, clustered mode over an ADO.NET store (one node fires each trigger).
- **Hangfire**: fire-and-forget, delayed, recurring and continuation jobs from lambdas, with a dashboard and automatic retries; SQL Server/PostgreSQL/Redis storage.
- Need cross-service messaging semantics? Use a broker (see MassTransit / Service Bus skill) rather than a job library.

## Quartz
```csharp
builder.Services.AddQuartz(q => {
    q.UsePersistentStore(s => { s.UseProperties = true; s.UseSqlServer(cs); s.UseClustering(); s.UseSystemTextJsonSerializer(); });
    var key = new JobKey("report");
    q.AddJob<ReportJob>(key, j => j.StoreDurably());
    q.AddTrigger(t => t.ForJob(key).WithCronSchedule("0 0 2 * * ?", c => c.WithMisfireHandlingInstructionFireAndProceed().InTimeZone(TimeZoneInfo.Utc)));
});
builder.Services.AddQuartzHostedService(o => o.WaitForJobsToComplete = true);
[DisallowConcurrentExecution] public class ReportJob(IReportService svc) : IJob { public Task Execute(IJobExecutionContext c) => svc.RunAsync(c.CancellationToken); }
```
## Hangfire
```csharp
builder.Services.AddHangfire(c => c.UseSqlServerStorage(cs)); builder.Services.AddHangfireServer();
BackgroundJob.Enqueue<IEmailer>(x => x.SendWelcome(userId));           // args serialised: pass ids, not entities
RecurringJob.AddOrUpdate<IReportService>("daily", x => x.Run(), Cron.Daily);
[AutomaticRetry(Attempts = 5, OnAttemptsExceeded = AttemptsExceededAction.Fail)]
```
Secure the dashboard (`DashboardOptions.Authorization`), never expose it anonymously.

## StackExchange.Redis
```csharp
var mux = await ConnectionMultiplexer.ConnectAsync("host:6380,ssl=true,abortConnect=false");   // one shared multiplexer per app (singleton)
var db = mux.GetDatabase();
await db.StringSetAsync("k", "v", TimeSpan.FromMinutes(5), When.NotExists);                  // SET NX EX: simple lock/dedupe (add unique token; release via Lua compare-and-delete)
```
For distributed locks prefer RedLock.net / DB advisory locks and always use fencing/idempotent jobs. Pub/sub is fire-and-forget (no persistence); use Streams for durable consumption. In .NET 9 use `HybridCache` over Redis for caching.

## Gotchas
- At-least-once execution: jobs must be idempotent; long jobs honour cancellation.
- Serialised job arguments break on refactoring signatures with queued jobs in storage.
- Clock/time zones for cron; DST gaps.
- Scoped services: resolve within a scope per job (Quartz and Hangfire do this for DI jobs).

## Verify
Run two instances: the recurring job fires once per schedule; kill a node mid-job and observe retry/recovery.
