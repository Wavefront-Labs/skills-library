---
id: computing-software.software-engineering.software-architecture.decorator-pattern
name: decorator-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, decorator-pattern, gof, wrapper, middleware, cross-cutting-concerns, composition-over-inheritance]
level: practitioner
status: draft
description: "Use the GoF Decorator to add behaviour (caching, retries, logging, metrics) by wrapping an object with the same interface, instead of subclass explosions."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Decorator", "https://refactoring.guru/design-patterns/decorator"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Decorator

**Intent (GoF):** attach additional responsibilities to an object dynamically; a
flexible alternative to subclassing for extending functionality.

## When it fits
Cross-cutting behaviour layered around a core: caching, retries, timing/metrics,
authorization checks, logging, compression, buffering. Combinations would otherwise
need a subclass per combination (`CachedRetryingLoggingRepo`).

## Shape
```go
type Store interface { Get(ctx context.Context, id string) (Item, error) }

type cachedStore struct { next Store; cache *lru.Cache[string, Item] }
func (c *cachedStore) Get(ctx context.Context, id string) (Item, error) {
    if it, ok := c.cache.Get(id); ok { return it, nil }
    it, err := c.next.Get(ctx, id)
    if err == nil { c.cache.Add(id, it) }
    return it, err
}

type timedStore struct { next Store; hist metrics.Histogram }
func (t *timedStore) Get(ctx context.Context, id string) (Item, error) {
    start := time.Now(); defer func() { t.hist.Observe(time.Since(start).Seconds()) }()
    return t.next.Get(ctx, id)
}

var s Store = &timedStore{next: &cachedStore{next: pgStore, cache: c}, hist: h}
```
Order matters: here timing measures cache hits too; swap the nesting to time only
database calls.

## Familiar instances
`java.io.BufferedInputStream(new FileInputStream(...))`, HTTP middleware
(`func(http.Handler) http.Handler`), Python function decorators (same idea at function
level), .NET `DelegatingHandler` for HttpClient, Scrutor `Decorate<>` in DI.

## Rules
- Decorator implements the same interface and forwards everything it doesn't change.
  Large interfaces make this painful (consider splitting the interface).
- Keep each decorator single-purpose; compose them at the composition root.
- Identity: code that checks concrete types (`instanceof PgStore`) breaks; avoid that.

## Verify
- [ ] Each decorator has a unit test with a fake inner implementation.
- [ ] Wiring order is documented where it matters (auth before cache, etc.).
