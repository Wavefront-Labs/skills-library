---
id: computing-software.data-engineering.druid.druid-granularities
name: druid-granularities
category: computing-software
field: data-engineering
product: druid
tags: [granularity, query-granularity, segment-granularity, iso8601-period, time-buckets]
level: practitioner
status: docs-checked
description: "Choose simple, duration or ISO8601 period granularities."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/granularities.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Granularity buckets data across time, used in native queries for result buckets and in `granularitySpec` for `segmentGranularity` and `queryGranularity`. Specify it as a simple string, a duration in milliseconds, or an arbitrary ISO8601 period.

Simple granularities are strings that bucket by UTC time, so days start at 00:00 UTC: `all`, `none`, `second`, `minute`, `five_minute`, `ten_minute`, `fifteen_minute`, `thirty_minute`, `hour`, `six_hour`, `eight_hour`, `day`, `week`, `month`, `quarter` and `year`. Use a period or duration granularity when you need other boundaries or time zones.

The same formats apply to ingestion. This page covers native queries; Druid SQL has its own time functions.

The same granularity strings are accepted for `segmentGranularity` and `queryGranularity` in the ingestion `granularitySpec`.
- `all` buckets everything into a single bucket. `none` is not zero bucketing: it buckets to millisecond granularity, the granularity of the internal index (think of it as `millisecond`). Do not use `none` in a timeseries query: Druid fills empty interior time buckets with zeroes, so the output would contain every millisecond in the interval.
- Avoid `week` for partitioning at ingestion time: weeks do not align with months and years, which makes it hard to partition by coarser granularities later.
- Duration granularity: `{"type": "duration", "duration": 7200000}` (milliseconds; timestamps returned as UTC) with an optional `origin` (default 1970-01-01T00:00:00Z) for where to start counting buckets.
- Period granularity: ISO8601 periods of years, months, weeks, hours, minutes and seconds (for example `P2W`, `P3M`, `PT1H30M`), such as `{"type": "period", "period": "P2D", "timeZone": "America/Los_Angeles"}`. `timeZone` (default UTC) sets where period boundaries start and the time zone of returned timestamps; `origin` is optional. Years start on 1 January, months on the first of the month, and weeks on Mondays unless an origin is given. Time zones are the IANA zones via Joda Time. Query intervals are not converted to the granularity's time zone.
- Empty buckets are discarded in groupBy results (the page's example).

## Checked

Confirmed against the Druid docs page "Query granularities": the list of simple granularity strings, UTC bucketing, none and all semantics, the week footnote, duration and period forms with origin and time zone defaults. Replaced the earlier vague "read the footnote" with the footnote's content.

Method: docs-only read of cited pages, 2026-11-08
