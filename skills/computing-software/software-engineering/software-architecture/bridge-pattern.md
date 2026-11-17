---
id: computing-software.software-engineering.software-architecture.bridge-pattern
name: bridge-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, structural-patterns, bridge-pattern, gof, abstraction-implementation, class-explosion, pimpl, composition-over-inheritance]
level: advanced
status: draft
description: "Use the GoF Bridge to separate an abstraction hierarchy from its implementation hierarchy so both vary independently, avoiding a subclass per combination."
sources: ["Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Bridge", "https://refactoring.guru/design-patterns/bridge", "https://en.cppreference.com/w/cpp/language/pimpl"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bridge

**Intent (GoF):** decouple an abstraction from its implementation so that the two can
vary independently.

## The problem it solves
Two independent dimensions of variation encoded in one inheritance tree multiply:
`Notification` x channel -> `UrgentEmailNotification`, `UrgentSmsNotification`,
`DigestEmailNotification`, `DigestSmsNotification`... N x M classes.

## Shape
```kotlin
// Implementation side: HOW to deliver
interface Channel { fun send(to: Recipient, subject: String, body: String) }
class EmailChannel(private val smtp: Smtp) : Channel { ... }
class SmsChannel(private val sms: SmsApi) : Channel { override fun send(to: Recipient, subject: String, body: String) = sms.send(to.phone, "$subject: $body".take(160)) }

// Abstraction side: WHAT kind of notification
abstract class Notification(protected val channel: Channel) { abstract fun notify(to: Recipient, event: Event) }
class UrgentNotification(ch: Channel) : Notification(ch) {
    override fun notify(to: Recipient, event: Event) = channel.send(to, "URGENT ${event.title}", event.details)
}
class DigestNotification(ch: Channel) : Notification(ch) { ... batches events ... }

val n = UrgentNotification(SmsChannel(api))      // N + M classes, combined at runtime
```

## Recognising it in the wild
- JDBC: `java.sql` API (abstraction) bridges to vendor drivers (implementation).
- Logging facades (SLF4J) over backends (Logback, Log4j2).
- Graphics APIs over platform renderers.
- C++ pimpl idiom: a class holds a pointer to an implementation class, hiding it from
  the header (ABI stability, faster compiles); a degenerate bridge with one implementation.

## Bridge vs Strategy vs Adapter
- Strategy swaps an ALGORITHM inside one context; Bridge structures two whole hierarchies.
- Adapter retrofits incompatible interfaces after the fact; Bridge is designed up front.

## Pitfalls
Applying it with only one real dimension of variation adds indirection for nothing.
Introduce when the second dimension actually appears (refactor: replace subclass with
delegate).

## Verify
- [ ] Adding a new channel requires no new notification classes, and vice versa.
