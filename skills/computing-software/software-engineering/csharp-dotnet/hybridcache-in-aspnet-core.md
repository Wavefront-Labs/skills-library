---
id: computing-software.software-engineering.csharp-dotnet.hybridcache-in-aspnet-core
name: hybridcache-in-aspnet-core
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-request-pipeline, hybridcache, stampede-protection, idistributedcache, memorycache, cache-tags]
level: advanced
status: docs-checked
description: "Use HybridCache (Microsoft.Extensions.Caching.Hybrid) for two-level caching with stampede protection, tag invalidation, serializers and a Redis secondary cache."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HybridCache in ASP.NET Core

## Setup
```bash
dotnet add package Microsoft.Extensions.Caching.Hybrid
```
```csharp
builder.Services.AddHybridCache(o => {
    o.MaximumPayloadBytes = 1024 * 1024;
    o.MaximumKeyLength = 1024;
    o.DefaultEntryOptions = new HybridCacheEntryOptions {
        Expiration = TimeSpan.FromMinutes(5),
        LocalCacheExpiration = TimeSpan.FromMinutes(5)
    };
});
builder.Services.AddStackExchangeRedisCache(o => o.Configuration = cs);   // optional secondary cache
```
```csharp
await cache.GetOrCreateAsync($"product:{id}",
    async token => await LoadAsync(id, token),
    entryOptions, tags: ["products"], cancellationToken: ct);
await cache.RemoveAsync($"product:{id}", ct);
await cache.RemoveByTagAsync("products", ct);
```

## What the page states
- Pages apply to ASP.NET Core 9.0 and later; the library also supports older runtimes down to .NET Framework 4.7.2 and .NET Standard 2.0.
- `GetOrCreateAsync` checks the primary (in-process `MemoryCache` by default) cache, then the secondary (`IDistributedCache`) if configured, then calls the factory and stores in both. Only one concurrent caller per key per `HybridCache` instance runs the factory; others wait. This does not coordinate across instances, even with the same distributed cache. The factory token is cancelled when all waiting callers cancel.
- Without an `IDistributedCache`, HybridCache still gives in-process caching and stampede protection. `AddDistributedMemoryCache` is not used as the secondary cache when the primary is the default `MemoryCache`.
- Keys are opaque strings. Do not use raw user input as keys (security and cache-flooding risk). The default maximum key length is 1024; longer keys bypass the cache (logged). `MaximumPayloadBytes` default is 1 MB; larger values are logged and not stored.
- `SetAsync` stores without reading. `RemoveAsync` removes from both caches (current server and secondary); other servers' in-memory caches are not affected.
- Tags: `RemoveByTagAsync` is logical, an "ignore anything created before now" rule; old values remain until they expire. `*` is reserved and invalidates everything; no glob matching; tags cannot be empty/whitespace.
- Serialization: `string` and `byte[]` handled internally, `System.Text.Json` for everything else; `AddSerializer<T,TSerializer>()` and `AddSerializerFactory` plug in others (protobuf example).
- Object reuse: by default each caller gets its own deserialised instance. Mark a type `sealed` and `[ImmutableObject(true)]` to tell HybridCache it can reuse instances.
- Optional `IBufferDistributedCache` support in preview Redis, SQL Server and Postgres cache packages avoids `byte[]` allocations.
- Native AOT needs source-generated or AOT-compatible serializers.

## Not covered by this page (the output-caching and distributed-caching pages were not read)
- Comparisons with `IMemoryCache`, `IDistributedCache` and output caching, and anything about exceptions from the factory being uncached, should be treated as unverified here.

## Verify
Fire parallel requests for a cold key with a counter in the factory and assert it ran once.

## Checked
Method: 2026-11-08 docs-only read of the HybridCache page. Dropped the other two cited pages (output and distributed caching) as unread. Removed unsupported claims: the "default recommendation on .NET 9+" line, "preview packages in the .NET 8 era", "factory exceptions are not cached", null-vs-missing advice and the comparison list; corrected the default `LocalCacheExpiration` example and added the MaximumKeyLength option.
