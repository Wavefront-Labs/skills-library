---
id: computing-software.software-engineering.csharp-dotnet.exception-handling-and-filters
name: exception-handling-and-filters
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-exceptions, exception-filters, throw-vs-throw-ex, custom-exceptions, exceptiondispatchinfo, error-handling, csharp-exception-handling]
level: practitioner
status: docs-checked
description: "Handle exceptions in C# properly: catch specific types, exception filters with when, throw vs throw ex, inner exceptions, custom exception design and global handlers."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/exception-handling-statements", "https://learn.microsoft.com/en-us/dotnet/standard/exceptions/how-to-create-user-defined-exceptions"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Exception handling and filters

**Goal:** exceptions that keep their stack traces, are caught only where they can be
handled, and report enough context.

## Catch narrowly
```csharp
try
{
    await client.SendAsync(request, ct);
}
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests)
{
    await Task.Delay(RetryAfter(ex), ct);
}
catch (OperationCanceledException) when (ct.IsCancellationRequested)
{
    throw;                                     // caller cancelled: let it flow
}
```
Exception filters (`when`) run **before** the stack unwinds: if false, the exception continues
as if not caught, and crash dumps still show the original throw site. Filters are also
used for logging without catching: `catch (Exception ex) when (Log(ex)) { }` where `Log`
returns false.

## Rethrowing
```csharp
catch (Exception ex)
{
    logger.LogError(ex, "Import of {File} failed", path);
    throw;                 // preserves stack trace
    // throw ex;           // resets the stack trace to here - CA2200
}
```
Wrap only to add meaning, keeping the cause:
`throw new ImportException($"Import of {path} failed", ex);`. To rethrow an exception captured
earlier (another thread): `ExceptionDispatchInfo.Capture(ex).Throw();`.

## Custom exceptions
```csharp
public sealed class InsufficientFundsException : Exception
{
    public InsufficientFundsException(decimal shortfall)
        : base($"Insufficient funds: short by {shortfall:C}") => Shortfall = shortfall;
    public InsufficientFundsException(string message, Exception inner) : base(message, inner) { }
    public decimal Shortfall { get; }
}
```
Name ends in `Exception`; derive from `Exception`; add properties
callers can act on.

## Exceptions vs control flow
- Use `TryParse` / `TryGetValue` patterns for expected failures; exceptions are expensive
  (stack capture) and obscure flow.
- Throw guard exceptions with helpers: `ArgumentNullException.ThrowIfNull(x)`,
  `ArgumentOutOfRangeException.ThrowIfNegative(n)`, `ObjectDisposedException.ThrowIf(_disposed, this)`.
- `finally`/`using` for cleanup; never swallow with an empty catch.

## Global handlers
ASP.NET Core: `app.UseExceptionHandler()` + `IExceptionHandler` -> ProblemDetails.
Workers/console: `AppDomain.UnhandledException` (log it),
`TaskScheduler.UnobservedTaskException` for forgotten tasks.

## Verify
- [ ] No `throw ex;` (CA2200) or `catch (Exception) { }` without rethrow/log (CA1031 reviewed).
- [ ] Wrapped exceptions carry `InnerException`.

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (exception-handling statements, best practices, error-handling pages): exception filters, throw vs throw ex (CA2200), IExceptionHandler, AppDomain.UnhandledException, TaskScheduler.UnobservedTaskException.
- Removed: ApplicationException remark, serialization-constructor note, .NET 8 version tag, process-dies remark.
Method: documentation only; no commands were run.
