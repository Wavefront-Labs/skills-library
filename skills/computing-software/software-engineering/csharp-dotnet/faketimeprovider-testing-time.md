---
id: computing-software.software-engineering.csharp-dotnet.faketimeprovider-testing-time
name: faketimeprovider-testing-time
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-testing-practice, faketimeprovider, timeprovider, testing-time, deterministic-tests, periodic-timer]
level: practitioner
status: docs-checked
description: "Make time-dependent .NET code testable with TimeProvider and FakeTimeProvider: injection, advancing the clock, fake timers, delays and cancellation sources without sleeping."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.timeprovider", "https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.time.testing.faketimeprovider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TimeProvider and FakeTimeProvider

```csharp
public class TokenService(TimeProvider clock)
{
    public bool IsExpired(Token t) => clock.GetUtcNow() >= t.ExpiresAt;
}
builder.Services.AddSingleton(TimeProvider.System);          // production registration

[Fact] public void Token_expires()
{
    var fake = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
    var svc = new TokenService(fake);
    var t = new Token(fake.GetUtcNow().AddMinutes(5));
    Assert.False(svc.IsExpired(t));
    fake.Advance(TimeSpan.FromMinutes(5));                   // no sleeping
    Assert.True(svc.IsExpired(t));
}
```

## What the pages state
- `TimeProvider` is an abstract class "providing an abstraction for time", in System.Runtime (.NET 8+) and in the `Microsoft.Bcl.TimeProvider` package for .NET Framework 4.6.2+ and .NET Standard 2.0.
- Members: `System` (real clock based on `DateTimeOffset.UtcNow`, `TimeZoneInfo.Local`, `Stopwatch` timestamps and `Timer`), `GetUtcNow`, `GetLocalNow`, `LocalTimeZone`, `GetTimestamp`, `TimestampFrequency`, `GetElapsedTime`, `CreateTimer`.
- Extension methods `CreateCancellationTokenSource(TimeProvider, TimeSpan)` and `Delay(TimeProvider, TimeSpan, CancellationToken)` take a provider. `PeriodicTimer` has a `(TimeSpan, TimeProvider)` constructor (PeriodicTimer page).
- `FakeTimeProvider` (namespace Microsoft.Extensions.Time.Testing, package Microsoft.Extensions.TimeProvider.Testing) derives from `TimeProvider` for "deterministic behavior in tests". Constructors: parameterless and `(DateTimeOffset)`. Members: `Advance(TimeSpan)`, `SetUtcNow`, `AdjustTime`, `SetLocalTimeZone`, `AutoAdvanceAmount` (time advances whenever the clock is read), `Start`, `CreateTimer`.

## Practitioner notes (not stated on the pages)
- Inject `TimeProvider` and avoid `DateTime.UtcNow` in domain code; store UTC.
- `Task.Delay(ms)` without the provider overload does not use the fake; use the `TimeProvider` overload.
- Advancing a large span may fire periodic timers repeatedly; check expectations.
- Integrations with `MemoryCache` and Polly were not verified on these pages.

## Verify
Tests with long timeouts complete in milliseconds because they advance a fake clock.

## Checked
Method: 2026-11-08 docs-only read of the TimeProvider and FakeTimeProvider reference pages (member lists and remarks). Removed unsupported claims: `WaitAsync(limit, clock)` usage, `MemoryCache` and Polly v8 integration, NodaTime remark, and the "await Task.Yield()" advice, and the fake-timer test sample.
