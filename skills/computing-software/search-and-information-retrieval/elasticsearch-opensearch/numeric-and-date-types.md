---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.numeric-and-date-types
name: numeric-and-date-types
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, numeric-and-date-types]
level: practitioner
status: docs-checked
description: "Pick numeric, scaled_float, date and range field types and avoid precision, parsing and identifier-mapping surprises (Elasticsearch reference)."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/number
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/date
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/range
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric, date and range field types

**Goal:** avoid precision, range and parsing surprises.
- Integer types `byte`, `short`, `integer`, `long`: pick the smallest that is enough, which helps indexing and searching efficiency; storage is optimized to the actual values, so the choice does not change storage size.
- Float types: `double` (53 significant bits), `float` (24), `half_float` (11, example loss `1.2345` to `1.234375`). `scaled_float` stores a long equal to the value times `scaling_factor` (required; e.g. 100 for cents), mostly to save disk space; a large factor or value can saturate at the long maximum and distort range queries.
- `double`, `float` and `half_float` treat `-0.0` and `+0.0` as different values in term and range queries.
- Identifiers (ISBN, product ID) rarely used in range queries are better as `keyword`: term queries on keyword are often faster. If unsure, map both with a multi-field.
- `ignore_malformed` defaults to `false`: a malformed number or date throws and rejects the whole document; when `true` the bad value is ignored. `coerce` (default `true`) converts strings to numbers.
- `date` is stored as a long of milliseconds since the epoch (UTC); use `date_nanos` for nanosecond resolution. Default `format` is `strict_date_optional_time||epoch_millis`; give several formats separated by `||` (the first is used to render values). For epoch seconds list `epoch_second`. Decimal-point epoch numbers can lose precision; avoid them.
- Range types (`integer_range`, `float_range`, `long_range`, `double_range`, `date_range`, `ip_range`) are indexed as objects with `gt`/`gte` and `lt`/`lte` bounds. A `range` query on them takes `relation`: `WITHIN`, `CONTAINS` or `INTERSECTS` (default). Sorting on a range field returns 400 Bad Request; only histogram and cardinality aggregations are supported.

```
{"mappings":{"properties":{"price":{"type":"scaled_float","scaling_factor":100},"day":{"type":"date","format":"strict_date_optional_time||epoch_millis"}}}}
```

## Verify
- [ ] A `range` query on the date field with `gte`/`gt` includes or excludes the edge date as intended.
- [ ] A `range` query with `"relation":"within"` on a `date_range` field returns only ranges fully inside the query bounds.

## Checked
2026-11-08. Confirmed against the Elasticsearch numeric, date and range field type pages: type sizes, smallest-type advice, scaled_float behaviour and saturation, signed-zero note, identifier-as-keyword advice, `ignore_malformed` and `coerce` defaults, date storage, default format, multiple formats, `epoch_second`, range type list, bounds, `relation` values, range sorting error and aggregation limits.
Removed: the claim that a mismatched date yields `mapper_parsing_exception` (docs say an exception rejects the document; the exact class is not stated), the "equality of floats rounding" remark, and the OpenSearch root source (OpenSearch pages were not checked).
Method: documentation only; no commands were run.
