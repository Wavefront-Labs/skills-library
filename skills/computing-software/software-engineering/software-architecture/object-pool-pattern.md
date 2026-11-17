---
id: computing-software.software-engineering.software-architecture.object-pool-pattern
name: object-pool-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, creational-patterns, object-pool-pattern, connection-pooling, resource-management]
level: practitioner
status: verified
description: "Apply the Object Pool pattern for expensive resources (connections, buffers, threads): sizing, borrowing and returning safely, validation, and when pooling hurts."
sources: ["https://sourcemaking.com/design_patterns/object_pool", "https://commons.apache.org/proper/commons-pool/", "https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing", "https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/how-to-create-an-object-pool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object Pool

Reuse instances that are expensive to create or limited in number instead of creating and
discarding them.

## Good candidates
Database/HTTP connections, threads (thread pools), large byte buffers (`ArrayPool<T>`, Netty
`PooledByteBufAllocator`, `sync.Pool` in Go), GPU contexts, licensed sessions.
Poor candidates: small ordinary objects in garbage-collected languages; modern GCs allocate them
cheaply, and pooling adds bugs and keeps garbage alive in old generations.

## Rules
- **Always return**: borrow in `try/finally`, `using`, `with`, or `defer`. Leaks exhaust the pool
  and requests hang waiting.
```python
with pool.connection() as conn:     # psycopg_pool
    conn.execute(...)
```
- **Reset state on return** (clear buffers, roll back open transactions, reset session variables);
  otherwise the next borrower sees stale or sensitive data.
- **Validate** before handing out or periodically (test query, `maxLifetime` shorter than the
  server/firewall idle timeout).
- **Bound** the pool and the wait (`connectionTimeout`): fail fast rather than queue forever.
- Size from measurement. HikariCP's pool-sizing wiki: connections = ((core_count * 2) + effective_spindle_count), core count excluding hyperthreads, spindle count near zero when the data set is cached;
  far fewer than most people configure. Total across all app instances must fit the DB's limit.
- Thread-safety: the pool must be; pooled objects are owned by one borrower at a time.
- Metrics: active, idle, waiting, wait time, timeouts.

## Use the existing one
HikariCP, pgbouncer/psycopg_pool, SQLAlchemy pool, Apache Commons Pool, .NET `ObjectPool<T>` /
`ArrayPool<T>`, Go `sync.Pool` (the Go source says any item may be removed automatically at any time without notification; for temporary buffers only). Write your own only for
domain resources no library covers.
