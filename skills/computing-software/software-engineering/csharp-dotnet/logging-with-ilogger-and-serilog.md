---
id: computing-software.software-engineering.csharp-dotnet.logging-with-ilogger-and-serilog
name: logging-with-ilogger-and-serilog
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ilogger, serilog, structured-logging, log-scopes, aspnet-core, opentelemetry-logs]
level: practitioner
status: docs-checked
description: "Log well in .NET: ILogger message templates (not interpolation), levels and category filters, scopes, LoggerMessage source generation, Serilog sinks and request logging."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/extensions/logging", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/logging/", "https://github.com/serilog/serilog-aspnetcore", "https://learn.microsoft.com/en-us/dotnet/core/extensions/logger-message-generator"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging with ILogger and Serilog

**Goal:** structured, queryable logs with the right volume, correlated per request.

## Message templates, not interpolation
```csharp
logger.LogInformation("Order {OrderId} placed by {CustomerId} for {Total:C}", order.Id, customer.Id, total);
// NOT: logger.LogInformation($"Order {order.Id} placed ...");
```
Templates keep `OrderId` as a queryable property and skip formatting when the level is
disabled. Interpolation allocates every time and flattens data into text (CA2254 warns).
Exceptions go first: `logger.LogError(ex, "Payment {PaymentId} failed", id)`.

## Levels and filtering
```json
"Logging": {
  "LogLevel": {
    "Default": "Information",
    "Microsoft.AspNetCore": "Warning",
    "Microsoft.EntityFrameworkCore.Database.Command": "Warning",
    "Acme.Billing": "Debug"
  }
}
```
Category = the `T` in `ILogger<T>` (full type name), so filters work by namespace prefix.
Change levels at runtime via config reload (`reloadOnChange`) without redeploying.

## Scopes
```csharp
using (logger.BeginScope(new Dictionary<string, object> { ["TenantId"] = tenant, ["JobId"] = job.Id }))
{
    logger.LogInformation("Starting import");       // carries TenantId and JobId
}
```
ASP.NET Core adds request scopes automatically when the provider has
`IncludeScopes` enabled (JSON console: `"FormatterOptions": { "IncludeScopes": true }`).

## High-performance logging
```csharp
[LoggerMessage(EventId = 1001, Level = LogLevel.Warning, Message = "Retrying {Url} attempt {Attempt}")]
static partial void LogRetry(ILogger logger, string url, int attempt);
```
No boxing, no template parsing per call; use in hot paths.

## Serilog
```csharp
builder.Host.UseSerilog((ctx, sp, cfg) => cfg
    .ReadFrom.Configuration(ctx.Configuration)
    .Enrich.FromLogContext()
    .WriteTo.Console());
app.UseSerilogRequestLogging();     // one summary line per request instead of several framework lines
```
Sinks: Seq, Elasticsearch, OpenTelemetry. 
## Hygiene
- Never log secrets, tokens, full request bodies or PII; redact classified data before it reaches the logger.
- JSON console output in containers; human-readable only locally.
- Log once at the boundary that handles an exception, not at every rethrow.

## Checked
2026-10-28: Confirmed in the .NET logging, ASP.NET Core logging and logger message generator pages and the serilog-aspnetcore README: message templates, LogLevel filtering by category, IncludeScopes, [LoggerMessage] partial methods, CA2254, UseSerilog/UseSerilogRequestLogging. Removed the JSON formatter name, the OpenTelemetry and Redaction package claims (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] No interpolated strings in log calls (CA2254 as error).
- [ ] Logs from one request share a TraceId and can be filtered by business keys.
