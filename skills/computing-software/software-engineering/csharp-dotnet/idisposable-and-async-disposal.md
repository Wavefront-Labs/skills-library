---
id: computing-software.software-engineering.csharp-dotnet.idisposable-and-async-disposal
name: idisposable-and-async-disposal
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, idisposable, iasyncdisposable, using-declaration, dispose-pattern, finalizer, httpclient, resource-leaks, safehandle]
level: practitioner
status: docs-checked
description: "Release .NET resources deterministically: using declarations, IAsyncDisposable, implementing Dispose correctly, DI-owned lifetimes, and the HttpClient trap."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose", "https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-disposeasync", "https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IDisposable and async disposal

**Goal:** files, sockets, DB connections and locks released at a known point, not
"whenever the GC gets round to it".

## Consuming disposables
```csharp
using var conn = new SqlConnection(cs);          // disposed at end of enclosing scope
await using var stream = File.OpenWrite(path);   // IAsyncDisposable: async flush/close
using (var tx = conn.BeginTransaction()) { ... } // block form for tighter scope
```
Prefer `await using` when the type implements IAsyncDisposable (streams, DbContext,
`Utf8JsonWriter`), so disposal does not block a thread on I/O.

## Implementing Dispose (sealed class, managed resources only: the common case)
```csharp
public sealed class Exporter : IDisposable, IAsyncDisposable
{
    private readonly Stream _out;
    private bool _disposed;
    public void Dispose() { if (_disposed) return; _disposed = true; _out.Dispose(); }
    public async ValueTask DisposeAsync() { if (_disposed) return; _disposed = true; await _out.DisposeAsync(); }
    private void ThrowIfDisposed() => ObjectDisposedException.ThrowIf(_disposed, this);
}
```
- Dispose must be idempotent and must not throw.
- No finalizer unless you DIRECTLY own an unmanaged handle; and then wrap the handle in
  a `SafeHandle` subclass instead of writing a finalizer.
- Unsealed base classes: the full `Dispose(bool disposing)` pattern +
  `GC.SuppressFinalize(this)`.

## Who disposes?
- You created it (`new`) -> you dispose it.
- DI container created it -> the container disposes it at scope end. Do NOT dispose
  injected services yourself.
- Transient disposables resolved from the ROOT provider are held until app shutdown (a
  leak). Resolve them inside a scope (`IServiceScopeFactory.CreateScope()`).

## HttpClient trap
`using var client = new HttpClient()` per request can exhaust sockets. Use
`IHttpClientFactory` (`services.AddHttpClient<MyApi>()`) or a single long-lived static
`HttpClient` with `SocketsHttpHandler { PooledConnectionLifetime = TimeSpan.FromMinutes(2) }`
so DNS changes are picked up.

## Gotchas
- Returning a disposable from inside a `using` block hands the caller a disposed object.
- Async methods: `using var x` stays alive until the method completes, possibly long
  after you need it; use a block to shorten.
- Analyzer CA2000 (dispose objects before losing scope) and CA2213 (disposable fields) catch leaks.

## Verify
- [ ] CA2000/CA2213 enabled with no violations.
- [ ] Load test: handle count / open sockets stay flat (`dotnet-counters`, `netstat`).

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (implementing Dispose and DisposeAsync, HttpClient guidelines, dependency injection guidelines): using declarations, IAsyncDisposable, container disposes what it creates, IServiceScopeFactory.CreateScope.
- Removed: TIME_WAIT detail.
Method: documentation only; no commands were run.
