---
id: computing-software.data-engineering.metabase.sql-time-grouping-parameters
name: sql-time-grouping-parameters
category: computing-software
field: data-engineering
product: metabase
tags: [time-grouping, sql-parameters, group-by, dashboard-filter, native-query]
level: practitioner
status: docs-checked
description: "Let viewers change time granularity in a Metabase SQL question using a time grouping parameter in both SELECT and GROUP BY, with defaults and aliasing rules."
sources:
  - https://www.metabase.com/docs/latest/questions/native-editor/time-grouping-parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A time grouping parameter lets users change how results group by time (day, week, month and so on).

Requirements: an aggregation such as `COUNT`, the parameter in the `SELECT` clause, and the same parameter in the `GROUP BY` clause.

```sql
SELECT COUNT(*) AS "Orders",
  {{created_at_param}} AS "Created At"
FROM orders
GROUP BY {{created_at_param}}
```

You can group by several time parameters, for example `{{created_at_param}}` and `{{trial_ends_at}}`.

Defaults: you can set a default such as "month", but values are limited to the time grouping options listed in the dashboard filters docs.

No value set: Metabase "won't group to a date part (like day or week)"; it just groups by untruncated dates.

Aliased tables: if you alias a table and map the parameter to a field in it, tell Metabase about the table and field alias, as with field filters.

Dashboards: the page only points to the dashboard filters docs for connecting the parameter to a dashboard filter.

As in all SQL groupings, the parameter must appear in both `SELECT` and `GROUP BY`.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Removed the unsupported dashboard datetime-summary claim and the invented database-error failure mode. Rest unchanged.
