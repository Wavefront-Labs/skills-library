---
id: computing-software.software-engineering.java.injectable-clock-for-testable-time
name: injectable-clock-for-testable-time
category: computing-software
field: software-engineering
product: java
tags: [java, java-time-api, injectable-clock, java-time-clock, clock-fixed, testable-time, spring-bean-clock]
level: practitioner
status: docs-checked
description: "Inject java.time.Clock instead of calling now() directly so tests control time with Clock.fixed/offset; wire it as a bean and tick forward manually."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/Clock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injectable Clock

**Problem:** `Instant.now()` and `LocalDate.now()` inside business logic make tests non-deterministic. The Clock API states the purpose: applications obtain the current time from an object rather than a static method, which can simplify testing, and alternative clocks such as `fixed` or `offset` can be used in tests.

## Production code takes a Clock
```java
public class TokenService {
    private final Clock clock;
    public TokenService(Clock clock) { this.clock = clock; }
    boolean expired(Token t) { return t.expiresAt().isBefore(Instant.now(clock)); }
    LocalDate today() { return LocalDate.now(clock); }   // zone comes from the clock
}
```
Wire `Clock.systemUTC()` (use it when you need the instant, not a date or time) or `Clock.systemDefaultZone()` as the production default. Both are immutable and thread-safe. With a DI container, expose it as a bean:
```java
@Bean Clock clock() { return Clock.systemUTC(); }
```

## Tests
```java
Clock fixed = Clock.fixed(Instant.parse("2026-11-03T12:00:00Z"), ZoneOffset.UTC);
var svc = new TokenService(fixed);

Clock later = Clock.offset(fixed, Duration.ofHours(2));     // base clock plus a fixed duration
```
For a clock that moves during a test, subclass `Clock`; its abstract methods are `getZone()`, `withZone(ZoneId)` and `instant()`. Implementations must be thread-safe, so make the mutable field `volatile` or atomic if the test uses threads:
```java
class MutableClock extends Clock {
    private Instant now; private final ZoneId zone;
    MutableClock(Instant start, ZoneId zone) { this.now = start; this.zone = zone; }
    void advance(Duration d) { now = now.plus(d); }
    @Override public ZoneId getZone() { return zone; }
    @Override public Clock withZone(ZoneId z) { return new MutableClock(now, z); }
    @Override public Instant instant() { return now; }
}
```

## Gotchas
- Every no-argument `now()` still uses the system clock in the default zone, so search the class for leftover calls.
- `Clock.tickMillis`, `tickSeconds`, `tickMinutes` and `tick(base, duration)` truncate the time to that granularity; do not use them where precision matters.

## Verify
A test advances the clock past expiry and asserts the state flips with no sleeping.

## Checked
Checked 2026-11-08 against the Java 21 Clock API page (class description, `fixed`, `offset`, `systemUTC`, `systemDefaultZone`, tick methods, abstract methods, thread-safety requirement).
Removed as unconfirmed: the forbiddenapis and ArchUnit enforcement tips, the remarks about `System.currentTimeMillis`, `Thread.sleep` and Awaitility, the `nanoTime` advice, and the dev.java date-time source (page not readable). The bean snippet is a usage example only; no Spring page was consulted.
Method: documentation only; no commands were run.
