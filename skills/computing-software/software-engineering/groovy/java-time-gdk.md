---
id: computing-software.software-engineering.groovy.java-time-gdk
name: java-time-gdk
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, java-time-gdk, groovy-datetime]
level: practitioner
status: docs-checked
description: "groovy-datetime GDK for java.time: format(String), static parse(value, pattern), plus and minus with TemporalAmount or integers, shift operators and duration DSL."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-datetime/src/spec/doc/_working-with-datetime-types.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# java.time with Groovy
The `groovy-datetime` module adds extensions for the Java 8 Date/Time API (the guide calls these "JSR 310 types").
- Formatting: `format(FormatStyle)` and `format(String pattern)` use `DateTimeFormatter`; for example pattern `'MM/dd/yyyy'` gives `03/10/2018`.
- Parsing: Groovy adds a static `parse` method to many JSR 310 types taking the value and then the pattern. This differs in argument order from the static `parse` Groovy added to `java.util.Date`, whose pattern comes first.
- `plus` and `minus` accept a `TemporalAmount`, so `+` and `-` work with `Period` and `Duration`. Integer overloads exist too; the unit depends on the type: days for `ChronoLocalDate` types such as `LocalDate`, years for `Year`, months for `YearMonth`, seconds for the rest (for example `LocalTime`).
- `*` multiplies `Period` and `Duration` by an integer, `/` divides a `Duration` by an integer, and unary `-` negates them. `++` and `--` step values by one unit.
- JSR 310 types work with the range operator. The `<<` operator combines two types into an aggregate type, and `>>` yields the `Period` or `Duration` between two values.
- A duration DSL gives `Duration` for time units (`1.hour`) and `Period` for date units (`2.months`).

## Checked

2026-11-03. Confirmed against the "Working with Date/Time types" section of the Groovy documentation (formatting and parsing, addition and subtraction, multiplication and division, increment, range, left shift and right shift, duration DSL). Removed: code snippets with asserted dates, the Date-versus-Instant `+` claim, the `ZoneId` advice, and the classpath note for slim builds.

Method: documentation only; no commands were run.
