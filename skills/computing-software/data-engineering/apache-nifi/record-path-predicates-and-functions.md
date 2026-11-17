---
id: computing-software.data-engineering.apache-nifi.record-path-predicates-and-functions
name: record-path-predicates-and-functions
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, record-path, predicates, functions, filter]
level: advanced
status: docs-checked
description: "RecordPath predicates and functions: comparison operators, filter functions like contains and matchesRegex, plus substring, replace, concat, format, coalesce, uuid5, mapOf."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/record-path-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predicates and functions

Predicates in brackets use `=`, `!=`, `>`, `>=`, `<`, `<=`:
- `/*[./state != 'NY']/zip`
- `/*[./state = /details/preferredState]`
- `/*/city[../state = 'NJ']`

Filter functions: `/name[contains(., 'o')]`, `/name[not(endsWith(., 'x'))]`, `/name[isEmpty(/details/employer)]`, `/name[isBlank(/details/phase)]`, `/name[matchesRegex(., '.* Doe')]`, `/id[ count(/elements[*]) = 2 ]`.

Standalone functions: `substring( /name, 0, -1 )`, `substringAfter( /name, ' ' )`, `replace( /name, 'o', 'x' )`, `replaceRegex(/name, '([JD])', '$1x')`, `concat( /name, ' lives in ', /homeAddress/city )`, `toUpperCase(/name)`, `toDate( /eventDate, "yyyy-MM-dd'T'HH:mm:ss'Z'" )`, `format( /eventDate, "yyyy-MM-dd" )`, `coalesce(/id, /name)`, `uuid5(/input)`, `escapeJson(/person)`, `mapOf("firstName", /firstName, "lastName", /lastName)`, `count(/elements[*])`, `recordOf("name", /firstName, "location", /address/city)`.

Verify: test each expression against sample records before deploying.

## Checked

Confirmed against the NiFi RecordPath Guide: predicate operators, relative paths in predicates, the filter functions (contains, matchesRegex, startsWith, endsWith, not, isEmpty, isBlank) and the standalone functions listed, each with the guide's example. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
