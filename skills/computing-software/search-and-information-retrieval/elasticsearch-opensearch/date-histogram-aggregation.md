---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.date-histogram-aggregation
name: date-histogram-aggregation
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, date-histogram-aggregation]
level: practitioner
status: docs-checked
description: "Bucket by calendar_interval or fixed_interval with time_zone, min_doc_count and extended_bounds."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-datehistogram-aggregation.html
  - https://docs.opensearch.org/latest/aggregations/bucket/date-histogram/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date histogram aggregation

**Goal:** time series buckets without gaps surprises.
- `{"aggs":{"per_day":{"date_histogram":{"field":"@timestamp","calendar_interval":"1d","time_zone":"Europe/London","min_doc_count":0}}}}`.
- `calendar_interval` is calendar-aware (day, month, year; `day` and `1d` are equivalent) and takes a single unit only: `2d` is an error. `fixed_interval` is an exact number of SI units (`30m`, `90m`, `12h`, `30d`) and cannot express months or quarters (`2w` and `month` are errors). Fractions such as `1.5h` are not supported; use `90m`.
- Bucketing is in UTC unless `time_zone` is set (an IANA name such as `Europe/Dublin`, or an offset such as `-01:00`); the bucket key stays UTC milliseconds. `offset` shifts bucket starts and is applied after the time zone.
- `min_doc_count` default is 0: empty buckets between the first and last matching documents are returned. `extended_bounds` ({"min","max"}) extends the range beyond the data; `hard_bounds` limits it.
- Sub-aggregations nest under the histogram for metrics per bucket.
- The legacy `interval` parameter is deprecated in OpenSearch; use `calendar_interval` or `fixed_interval`.
- Failure mode: a multiple in `calendar_interval` or a calendar unit in `fixed_interval` fails to parse.

## Verify
- [ ] Bucket boundaries at midnight local time and daylight saving transitions match expectations.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.

## Checked
2026-11-08. Read the Elasticsearch date histogram page (intervals, time_zone, offset, bounds) and the OpenSearch date histogram page (parameters table, deprecated `interval`, `min_doc_count` default). Removed the claim that mixing syntaxes errors in general; only the documented failure cases remain. Daylight saving bucket behaviour was not checked beyond the OpenSearch calendar interval note.
Method: documentation only; no commands were run.
