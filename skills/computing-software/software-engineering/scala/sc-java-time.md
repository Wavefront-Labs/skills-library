---
id: computing-software.software-engineering.scala.sc-java-time
name: sc-java-time
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-dates-time, java-time]
level: practitioner
status: draft
description: "Use java.time types, formatters and time zones instead of legacy Date."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# java.time usage in Scala
- Use `Instant`, `LocalDate`, `ZonedDateTime`, `Duration`, `DateTimeFormatter.ISO_LOCAL_DATE`; the types are immutable.
- Store instants in UTC, convert to a zone only for display: `instant.atZone(ZoneId.of("Europe/London"))`.
- `scala.concurrent.duration` (`5.seconds`) is separate from `java.time.Duration`.
- Scala.js needs `scala-java-time` for these types.
Verify: test around DST changes.
