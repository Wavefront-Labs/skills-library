---
id: computing-software.data-engineering.apache-nifi.expression-language-math-and-dates
name: expression-language-math-and-dates
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, expression-language, math, dates, format, todate]
level: practitioner
status: docs-checked
description: "NiFi Expression Language math and date functions: plus, minus, mod, toRadix, math(), random, now():format, toDate with time zone, toNumber epoch milliseconds."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Math and dates

Math:
- `${fileSize:plus(1000)}`, `${fileSize:minus(100)}`, `${fileSize:mod(12)}`
- `${fileSize:toRadix(16, 8)}` (hex padded to 8 characters)
- `${math("random")}`, `${literal(2):toDecimal:math("pow", 2.5)}`
- `${random():mod(10):plus(1)}`

Dates:
- Format a number as a date: `${time:format("yyyy/MM/dd", "GMT")}`, `${now():format('yyyy')}`
- Parse text: `${year:toDate('yyyy', 'GMT')}`
- Epoch milliseconds: `${now():toNumber()}`

The second argument of `format` and `toDate` is an optional time zone in Java TimeZone syntax; without it the local time zone is used. `format` expects a number of milliseconds since 1970-01-01 GMT.

Verify: evaluate against a known FlowFile and compare to the expected string or number.

## Checked

Confirmed against the NiFi Expression Language Guide: plus, minus, mod, toRadix (with padding), random, math (including `random` and `pow`), format, toDate, toNumber and now examples. Corrected `toDecimal()` to the guide's `toDecimal` form and made the time zone argument optional as documented.

Method: docs-only read of cited pages, 2026-11-08
