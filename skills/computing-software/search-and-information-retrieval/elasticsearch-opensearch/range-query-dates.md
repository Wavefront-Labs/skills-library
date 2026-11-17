---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.range-query-dates
name: range-query-dates
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, range-query-dates]
level: practitioner
status: docs-checked
description: "Query numbers and dates with range, gte/lte, format, time_zone and date math such as now-7d/d."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-range-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Range queries and date math

**Goal:** correct date ranges.
```
{"range":{"@timestamp":{"gte":"now-7d/d","lt":"now/d","time_zone":"+01:00"}}}
```
- Operators `gt`, `gte`, `lt`, `lte`; `format` overrides the field's mapped date format for the query values.
- `time_zone` accepts a UTC offset or IANA time zone. It does not affect `now`, which is always the current system time in UTC, but it does convert dates calculated with `now` and date math rounding (for example `now/d`).
- Date math rounding depends on the operator: `gt` rounds up to the first millisecond not covered by the rounded date; `gte` rounds down to the first millisecond; `lt` rounds down to the last millisecond before the rounded value; `lte` rounds up to the latest millisecond in the interval. For `2014-11-18||/M`: `gt` gives `2014-12-01T00:00:00.000`, `gte` gives `2014-11-01T00:00:00.000`, `lt` gives `2014-10-31T23:59:59.999`, `lte` gives `2014-11-30T23:59:59.999`.
- With no `format`, a numeric value on a `date` field is read as milliseconds since the epoch; pass a year such as `"2020"` as a string.
- Range queries on `text` or `keyword` fields do not run if `search.allow_expensive_queries` is `false`.

## Verify
- [ ] Count documents at the boundary timestamps and confirm the inclusion rules above.

## Scope
The Elasticsearch reference page was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference Range query page. Confirmed: all statements above. Removed: "rounding allows caching" (not on this page; see the request-cache page, which only says most `now` queries cannot be cached), "ranges on keyword/text are lexicographic" (not stated) and the OpenSearch source root.

Method: documentation only; no commands were run.
