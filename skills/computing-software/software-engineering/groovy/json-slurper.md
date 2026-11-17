---
id: computing-software.software-engineering.groovy.json-slurper
name: json-slurper
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, json-slurper, groovy-json]
level: practitioner
status: docs-checked
description: "Parse JSON with JsonSlurper: result types, parser variants selected with JsonParserType, and date-like string handling."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-json/src/spec/doc/json-userguide.adoc
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-json/src/main/java/groovy/json/JsonParserType.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing JSON with JsonSlurper
Type mapping from the user guide: JSON string to `String`, number to `BigDecimal` or `Integer`, object to `LinkedHashMap`, array to `ArrayList`, true/false to booleans, null to Groovy `null`, and a date to `java.util.Date` using the `yyyy-MM-dd'T'HH:mm:ssZ` format.
- Results conform to GPath expressions, so they can be navigated like other slurper results.
- Parser variants are chosen with `JsonSlurper#setType()` and the `JsonParserType` constants: `CHAR_BUFFER` (default, `JsonParserCharArray`), `INDEX_OVERLAY` (`JsonFastParser`), `LAX` (`JsonParserLax`, tolerates comments and unquoted strings) and `CHARACTER_SOURCE` (for very large files, over 2MB).
- `INDEX_OVERLAY` is the fastest but keeps pointers to the original buffer and defers object creation: take care before putting its maps in a long-term cache. The guide recommends it for buffers under 2MB.
- `INDEX_OVERLAY` and `LAX` return a `Date` for full ISO-8601 date-time strings; `setCheckDates(false)` turns that off. A date without a time, such as `"2026-09-04"`, stays a `String`.

## Checked

2026-11-03. Confirmed against the JSON user guide (type table, parser variants, date-like strings). Removed: code snippets, the claims about missing keys, large integer types and untrusted input limits.

Method: documentation only; no commands were run.
