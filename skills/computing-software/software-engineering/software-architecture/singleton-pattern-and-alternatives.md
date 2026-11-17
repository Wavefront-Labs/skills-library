---
id: computing-software.software-engineering.software-architecture.singleton-pattern-and-alternatives
name: singleton-pattern-and-alternatives
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, creational-patterns, singleton-pattern, gof, global-state, dependency-injection, lazy-initialization, testability]
level: practitioner
status: gated
description: "Know when a single instance is legitimate, implement it thread-safely when needed, and prefer DI-managed singletons over the GoF static-accessor Singleton."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Singleton", "Effective Java, 3rd ed. (Bloch), Item 3", "https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection#service-lifetimes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Singleton and its alternatives

**Intent (GoF):** ensure a class only has one instance, and provide a global point of
access to it.

## The problem with the classic form
The "global point of access" (`Config.getInstance()`) is the harmful half:
- hidden dependencies: function signatures lie about what they use;
- tests can't substitute it and leak state between tests;
- initialisation order and lifecycle (shutdown, reload) become implicit.
Having ONE instance is often fine; reaching it through a static accessor usually isn't.

## Preferred: single instance via composition root / DI
```csharp
builder.Services.AddSingleton<IClock, SystemClock>();          // one per container
builder.Services.AddSingleton<ConnectionMultiplexer>(_ => ConnectionMultiplexer.Connect(cs));
public class Billing(IClock clock) { ... }                      // dependency is explicit
```
(C# block not compiled here: no .NET SDK; (gated: unconfirmed, source is paywalled or blocked).)
Spring beans are singletons by default (Spring reference, bean scopes); in Go, construct once in `main` and pass down.

## When you truly need a language-level singleton
Process-wide resources with no reasonable injection path (a logging backend, a native
library handle). Make it lazy and thread-safe using the language's guarantees:
```java
public enum Registry { INSTANCE; ... }                         // Bloch: serialization- and reflection-safe
class Holder { static final Expensive VALUE = new Expensive(); } // lazy holder idiom: class init is thread-safe
```
(Java blocks and the Bloch Effective Java Item 3 attribution not run or read here: no JDK, book paywalled; (gated: unconfirmed, source is paywalled or blocked).)
```python
@functools.cache
def get_settings() -> Settings: return Settings()               # module-level lazy singleton
```
```go
var once sync.Once; var inst *Client
func Get() *Client { once.Do(func(){ inst = newClient() }); return inst }
```
The `functools.cache` and `sync.Once` snippets were run (Go: five goroutines calling `Get()` printed `init` once; the Python function body ran once). Avoid hand-written double-checked locking (easy to get wrong without `volatile`).

## Pitfalls
- Mutable singleton state shared across requests = concurrency bugs and cross-tenant leaks.
- Singleton depending on scoped services (DI "captive dependency"): holds a stale DbContext forever (not confirmed against Microsoft's docs here; (gated: unconfirmed, source is paywalled or blocked)).
- "One instance per process" breaks under multiple processes/pods; distributed
  uniqueness (leader election, locks) is a different problem.

## Verify
- [ ] No new `getInstance()`-style static accessors in application code; singletons registered in DI.
- [ ] Tests can replace each singleton with a fake.
