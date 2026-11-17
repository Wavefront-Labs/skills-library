---
id: computing-software.data-engineering.apache-nifi.record-path-navigation
name: record-path-navigation
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, record-path, records, paths, arrays, maps]
level: practitioner
status: docs-checked
description: "RecordPath navigation: child and descendant paths, wildcards, relative paths, array indexes and ranges, and map keys, used by UpdateRecord and similar record processors."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/record-path-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RecordPath navigation

- Child: `/details/address/zip`
- Descendant: `//zip`
- Wildcard: `/*`
- Relative (used inside predicates): `./name` (current field), `../state` (parent)
- Array: `/addresses[0]`, `/addresses[-1]`, `/addresses[0, 1, 2, 3]`, range `/addresses[0..8]`, `/addresses[0..-1]`, mixed `/addresses[0, 1, 4, 6..-1]`
- Map keys: `/details/address['zip']`, `/details/address['city', 'state', 'zip']`, all with `/details/address[*]`

Verify: run the path in the processor on sample data and confirm the selected field values.

## Checked

Confirmed against the NiFi RecordPath Guide: child operator, descendant operator, wildcard, array indexes including negative indexes and `..` ranges, map keys in quotes and the `[*]` wildcard. Relative paths start with `.` or `..` and are used in predicates.

Method: docs-only read of cited pages, 2026-11-08
