---
id: computing-software.software-engineering.go.dependency-injection-without-frameworks
name: dependency-injection-without-frameworks
category: computing-software
field: software-engineering
product: go
tags: [go, go-design-style, go-dependency-injection, dependency-injection, constructor-injection, wire]
level: practitioner
status: draft
description: "Wire Go applications with plain constructor injection in main, small consumer-side interfaces, and optional codegen (wire) only when graphs grow."
sources:
  - https://go.dev/doc/effective_go#interfaces
  - https://github.com/google/wire
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Dependency injection without frameworks

**Goal:** testable components with an obvious object graph.

```go
type Store interface { Get(ctx context.Context, id string) (Order, error) }   // defined by the consumer

type Service struct {
    store Store
    clock func() time.Time
    log   *slog.Logger
}
func NewService(s Store, log *slog.Logger) *Service {
    return &Service{store: s, clock: time.Now, log: log}
}

func main() {                              // composition root: the only place that knows concrete types
    db := mustOpenDB(cfg)
    svc := NewService(pg.NewStore(db), slog.Default())
    h := api.NewHandler(svc)
    run(cfg, h)
}
```

Guidelines: inject dependencies as constructor parameters, not package-level variables or `init()` side effects; accept interfaces at the consumer, return concrete types; keep interfaces to the methods actually used so fakes are 10 lines; pass `context.Context` and request data per call, not at construction. When `main` exceeds ~100 lines of wiring, `google/wire` generates it at build time (compile-time checked, no reflection); runtime reflection containers (`uber-go/dig`/`fx`) trade debuggability for convenience.

## Gotchas
- Global singletons (`var DB *sql.DB`) make tests order-dependent and parallel tests unsafe.
- Circular dependencies mean a missing abstraction; extract an interface in one package.
- Functional options (`WithTimeout`) suit optional configuration, constructor parameters suit required collaborators.

## Verify
Unit-test `Service` with an in-memory fake `Store` and `go test -race -shuffle=on`; the test file should not import the real database package.
