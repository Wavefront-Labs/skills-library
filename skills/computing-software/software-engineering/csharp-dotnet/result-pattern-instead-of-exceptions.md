---
id: computing-software.software-engineering.csharp-dotnet.result-pattern-instead-of-exceptions
name: result-pattern-instead-of-exceptions
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-exception-handling, result-pattern, error-handling, discriminated-unions, tryparse-pattern, railway-oriented]
level: practitioner
status: draft
description: "Model expected failures in C# as values with a Result<T> type or the Try pattern, reserving exceptions for bugs; mapping results to ProblemDetails and composing with pattern matching."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/handle-errors"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Result pattern

Exceptions are slow (tens of microseconds each plus stack capture) and hide failure paths. For **expected** outcomes (validation fails, not found, conflict) return a value; keep exceptions for the unexpected (bugs, I/O faults, invariants).

```csharp
public readonly record struct Error(string Code, string Message);

public readonly struct Result<T>
{
    private readonly T? _value; private readonly Error? _error;
    private Result(T v) { _value = v; _error = null; }
    private Result(Error e) { _value = default; _error = e; }
    public bool IsSuccess => _error is null;
    public static implicit operator Result<T>(T v) => new(v);
    public static implicit operator Result<T>(Error e) => new(e);
    public TOut Match<TOut>(Func<T, TOut> ok, Func<Error, TOut> fail) => _error is { } e ? fail(e) : ok(_value!);
}

Result<Order> Place(Cart c) => c.Items.Count == 0 ? new Error("cart.empty", "Cart is empty") : new Order(c);

return Place(cart).Match(
    ok: o => Results.Created($"/orders/{o.Id}", o),
    fail: e => e.Code switch {
        "cart.empty" => Results.Problem(title: e.Message, statusCode: 422),
        _            => Results.Problem(statusCode: 500) });
```
Alternatives: the BCL **Try pattern** (`bool TryParse(string, out T)`), nullable returns for lookups, or libraries (`ErrorOr`, `OneOf`, `FluentResults`). C# has no native discriminated unions yet; a closed hierarchy of records plus a `switch` expression gives exhaustiveness warnings.

## Guidelines
- One error vocabulary (codes, not messages) shared across layers; map once at the API edge to `ProblemDetails`.
- Do not return `Result` for programmer errors: use `ArgumentNullException.ThrowIfNull` and guards.
- Async: `Task<Result<T>>`; helper extensions (`Bind`, `Map`) avoid nested `Match`es but do not overbuild the DSL.

## Gotchas
- Swallowing exceptions into results loses stack traces; keep the inner exception on unexpected errors.
- Ignoring a returned `Result` silently drops failure; use `[MustUseReturnValue]`-style analyzers or `readonly struct` APIs that force handling.
- Overuse makes simple code verbose.

## Verify
Unit tests cover each error code mapping to the right HTTP status, and a benchmark shows no allocation on the failure path.
