---
id: computing-software.data-engineering.metabase.summarize-and-grouping
name: summarize-and-grouping
category: computing-software
field: data-engineering
product: metabase
tags: [summarize, grouping, binning, cumulative-sum, row-limit, query-builder]
level: practitioner
status: docs-checked
description: "Summarize and group in the Metabase query builder: metric types, cumulative needs, chained summaries, binning behaviour and the 10,000 row aggregated result cap."
sources:
  - https://www.metabase.com/docs/latest/questions/query-builder/summarizing-and-grouping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A summary has one or more metrics, optionally grouped by one or more columns.

Basic metrics: count of rows, sum, average, number of distinct values, cumulative sum, cumulative count of rows, standard deviation, minimum and maximum. Cumulative metrics need a date column grouping to be useful. You can also write a custom expression, or use admin-defined metrics or measures from the Metrics or Measures sections.

Chaining: you can add a second summarize step, with filters or joins in between.

Row limit: aggregated results are capped at 10,000 rows by default. The `MB_AGGREGATED_QUERY_ROW_LIMIT` environment variable changes this.

Grouping controls:
- Clicking another column replaces the current grouping; the plus icon adds one and the X removes one.
- Datetime: click "by month" to change granularity; the same column can be broken out at several granularities.
- Numeric columns bin automatically; you can set a fixed number of equal-width bins and empty bins are hidden. Custom bin ranges are not supported.
- Latitude and longitude bin automatically; set a degree size or turn binning off.

Default chart: the grouping column decides the default visualization, and a date grouping gives a line chart.

Bins: Metabase "will not display" empty intervals.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Replaced an inferred "failure mode" line with a page-stated point. Otherwise unchanged.
