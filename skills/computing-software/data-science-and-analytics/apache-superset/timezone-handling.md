---
id: computing-software.data-science-and-analytics.apache-superset.timezone-handling
name: timezone-handling
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [timezones, utc, timestamps, epoch, datetime]
level: intro
status: docs-checked
description: "Avoid Superset timezone bugs: keep database engine and backend in the same zone, preferably UTC, and know why epoch and zone-less timestamps differ."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/timezones.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make time filters and charts agree across servers.

Four timezone components touch Superset: the zone the data is encoded in, the zone of the database engine, the zone of the Superset backend, and the zone of the client. A temporal field (DATETIME, TIME, TIMESTAMP) with no explicit zone defaults to the underlying zone of the component.

Superset controls neither how data is ingested nor the client zone, so the docs recommend:
- Configure the database engine and the Superset backend to the same timezone, with a strong preference for UTC, so zone-less timestamps are not coerced into the wrong zone.
- Superset currently assumes timestamps are in UTC, so a non-UTC backend zone can be problematic.

How the backend tries to stay consistent: it ensures timestamps sent to the client carry an explicit zone, or a semi-explicit one such as epoch time, which is always relative to UTC.

Why engines differ: Superset reads SQL into a Pandas DataFrame before serializing to JSON, and Pandas ignores the DB-API type_code, using the Python type the driver returns. Only a subset of engines produce timestamps with the server zone. The docs' example: a MySQL `TIMESTAMP` comes out as epoch milliseconds (`1640995200000`, interpreted as UTC), while a Presto `TIMESTAMP` comes out as `"2022-01-01 00:00:00.000"` with no zone. JavaScript treats these differently: `new Date(1640995200000)` is a UTC instant shown in the client zone, whereas `new Date("2022-01-01 00:00:00.000")` is parsed as client-local time.

Practical consequence: when two clients or dashboards disagree on the same data, check whether the engine returns epoch values or zone-less strings, and compare the database engine and backend zones first.

## Checked

2026-11-08: read timezones.mdx in full. Removed claims the page does not make (per-user conversion statement, TZ on web and worker containers, relative filters computed from the server clock, AT TIME ZONE advice).
Method: documentation only; no commands were run.
