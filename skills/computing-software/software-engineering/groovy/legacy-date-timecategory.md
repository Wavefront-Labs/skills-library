---
id: computing-software.software-engineering.groovy.legacy-date-timecategory
name: legacy-date-timecategory
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, legacy-date-timecategory]
level: practitioner
status: docs-checked
description: "Work with java.util.Date in Groovy using the dateutil GDK methods (Date.parse, format, clearTime) and the TimeCategory duration DSL."
sources:
  - https://groovy-lang.org/groovy-dev-kit.html
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-dateutil/src/main/java/org/apache/groovy/dateutil/TimeCategory.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legacy Date and TimeCategory
- `TimeCategory` is a category: wrap the code in `use(TimeCategory) { ... }` and integers gain duration properties such as `days`, `day`, `hours` and `minutes` (`getDays(Integer)`, `getHours`, `getMinutes`). The metaprogramming chapter shows `use(TimeCategory)` blocks.
- Inside the block, `Date - Date` is `TimeCategory.minus(Date, Date)` and returns a `TimeDuration`; `Date - duration` returns a `Date` (`minus(Date, BaseDuration)`).
- The GDK adds a static `Date.parse(format, input)` (the Groovy Development Kit page shows `Date.parse('yyyy-MM-dd', '2000-01-01')`).
- `DateUtilExtensions` (the dateutil module) supplies `format(...)` and `clearTime()` on `Date` and uses `SimpleDateFormat` internally.
- For new code, the `groovy-datetime` module works on the `java.time` types instead (see the java-time-gdk skill).

## Checked

2026-11-03. Confirmed against the `TimeCategory` and `DateUtilExtensions` sources (method names and return types), the Groovy Development Kit page (`Date.parse` examples) and the Metaprogramming chapter (`use(TimeCategory)`). Removed: `TimeDatumDependentDuration` details, thread-safety and leniency claims about `SimpleDateFormat`, the deprecation claim, and the code snippets and self-check.

Method: documentation only; no commands were run.
