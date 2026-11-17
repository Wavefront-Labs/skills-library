---
id: computing-software.software-engineering.csharp-dotnet.loggermessage-source-generator
name: loggermessage-source-generator
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-observability, loggermessage-generator, loggermessage, structured-logging, ilogger, high-performance-logging]
level: practitioner
status: docs-checked
description: "Use [LoggerMessage] source-generated logging: partial methods, event ids, levels, templates, exception handling, dynamic levels, redaction, and the CA1848 analyzer."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/extensions/logger-message-generator", "https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1848", "https://learn.microsoft.com/en-us/dotnet/core/extensions/data-redaction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LoggerMessage source generator

```csharp
public static partial class Log
{
    [LoggerMessage(EventId = 1001, Level = LogLevel.Information, Message = "Order {OrderId} placed for {Customer}")]
    public static partial void OrderPlaced(this ILogger logger, long orderId, string customer);

    [LoggerMessage(EventId = 1002, Level = LogLevel.Error, Message = "Payment failed for {OrderId}")]
    public static partial void PaymentFailed(this ILogger logger, Exception ex, long orderId);
}
_logger.OrderPlaced(order.Id, order.CustomerName);
```
Instance form: a `partial` method in a `partial` class uses the class's `ILogger` field (from .NET 9, an `ILogger` primary-constructor parameter; the field wins if both exist). A static method needs the `ILogger` as a parameter.

## What the docs state
- The generator builds on `ILogger` and `LoggerMessage.Define`; the docs say it is considerably faster at runtime and eliminates boxing, temporary allocations and copies as far as possible.
- Constraints: methods must be `partial` and return `void`; method and parameter names must not start with an underscore; no `params`, `scoped` or `out` parameters, no `ref struct` parameters; generics supported except the C# 13 `allows ref struct` anti-constraint. Needs C# 9 or later.
- The first `ILogger`, `LogLevel` and `Exception` parameters are treated specially; later ones are ordinary template arguments. Do not put a placeholder for the exception parameter in the template (a diagnostic is raised).
- Omit `Level` from the attribute and take a `LogLevel` parameter for a dynamic level. `EventName` sets the event name. Format specifiers such as `{Value:E}` work.
- Placeholder names are matched case-insensitively with parameter names; parameter order need not match template order.
- `Message` is optional; parameters without placeholders raise SYSLIB1015 and are stored in log state but not in the formatted text.
- The generator warns on duplicate event IDs.
- Benefits over `LoggerMessage.Define`: simpler syntax, any number of parameters (Define supports six), dynamic level.
- CA1848 flags logger extension methods such as `LogInformation` and recommends `LoggerMessage`; it says extension methods box value types and re-parse the template each call, while `LoggerMessage` parses once. It is not enabled by default in .NET 10, and the page says not to suppress it.
- Redaction: `Microsoft.Extensions.Compliance.Redaction` provides redactors (ErasingRedactor, HmacRedactor, custom) chosen by data classification; with `Microsoft.Extensions.Telemetry`, `builder.EnableRedaction()` and a classification attribute on the log parameter redact before output. HmacRedactor is experimental (EXTEXP0002). Review logs regularly.

## Not stated on the cited pages
- The generated code's `IsEnabled` pre-check and the `SkipEnabledCheck` option; a "`[LogProperties]`" attribute; `FakeLogger<T>` testing; CA2254. Treat these as unverified here.

## Verify
Build without CA1848 warnings; assert on captured log records in a test logger.

## Checked
Method: 2026-11-08 docs-only read of the source-generation (logger-message-generator), CA1848 and data-redaction pages. Removed unsupported claims: cached-delegate/IsEnabled description, SkipEnabledCheck, `[LogProperties]`, "not generic before .NET 7", SYSLIB1006, FakeLogger and CA2254 notes. Added documented constraints, .NET 9 primary-constructor support and redaction details.
