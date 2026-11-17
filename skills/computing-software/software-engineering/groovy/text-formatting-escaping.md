---
id: computing-software.software-engineering.groovy.text-formatting-escaping
name: text-formatting-escaping
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, text-formatting-escaping]
level: practitioner
status: draft
description: "String.format, sprintf, printf, formatting numbers, and escape helpers like StringEscapeUtils (from groovy-templates / commons)."
sources:
  - https://docs.groovy-lang.org/latest/html/groovy-jdk/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formatting and escaping text
- `String.format('%05.2f', 3.14159)`, `sprintf('%s=%d', 'a', 1)`, `printf('%-10s|%n', 'x')`.
- `'%,d'.format(1234567)` gives grouping using default locale: pass a `Locale` for stable output.
- For HTML/JSON/SQL use the proper encoder (`JsonOutput.toJson`, PreparedStatement) instead of manual escapes.
- `groovy.xml.XmlUtil.escapeXml(s)` escapes XML text.

## Gotchas
- Default locale changes decimals and grouping: pin `Locale.ROOT` in tests.
- Never build SQL or shell strings by interpolation (injection risk).

## Self-check
`assert sprintf('%05.1f', 3.14159) == '003.1'`.
