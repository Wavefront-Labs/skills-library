---
id: computing-software.software-engineering.software-architecture.proxy-pattern
name: proxy-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, proxy-pattern, gof, lazy-loading, remote-proxy, protection-proxy, dynamic-proxy, aop]
level: practitioner
status: draft
description: "Use the GoF Proxy (virtual, remote, protection, caching) to control access to an object, and understand framework dynamic proxies such as Spring AOP and ORM lazy loading."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Proxy", "https://docs.spring.io/spring-framework/reference/core/aop/proxying.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/reflect/Proxy.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proxy

**Intent (GoF):** provide a surrogate or placeholder for another object to control
access to it.

## Kinds
| Proxy | Controls | Example |
|---|---|---|
| Virtual | creation (lazy load expensive object) | Hibernate lazy association proxies, image placeholders |
| Remote | location (object in another process) | gRPC stubs, RMI, COM |
| Protection | permissions | check caller rights before delegating |
| Smart reference / caching | extra bookkeeping | ref-counting (`shared_ptr`), memoising results |

Structurally like Decorator (same interface, wraps a subject). Difference is intent:
proxy controls ACCESS to the subject and often manages its lifecycle; decorator adds
behaviour.

## Hand-written virtual proxy
```java
class LazyReport implements Report {
    private final Supplier<Report> loader; private Report real;
    LazyReport(Supplier<Report> loader) { this.loader = loader; }
    public String render() { if (real == null) real = loader.get(); return real.render(); }
}
```
(Add synchronisation if shared across threads.)

## Framework dynamic proxies: know their traps
Spring `@Transactional`, `@Cacheable`, `@Async` work via proxies around beans:
- **Self-invocation bypasses the proxy**: calling `this.save()` from another method in the
  same bean skips the transaction. Move the method to another bean or inject self.
- JDK proxies only proxy interface methods; CGLIB proxies can't intercept `final` or
  private methods.
Hibernate lazy proxies:
- Accessing a lazy association after the session closes -> `LazyInitializationException`.
- `getClass()` returns the proxy subclass; equals implementations must use
  `instanceof`/Hibernate.getClass.
Python: `__getattr__` delegation gives simple proxies; `wrapt.ObjectProxy` handles edge cases.

## Verify
- [ ] No self-invocation of proxied annotations (`@Transactional` methods called via `this`).
- [ ] Lazy proxies are not touched outside their session/transaction (tests with lazy loading enabled).
