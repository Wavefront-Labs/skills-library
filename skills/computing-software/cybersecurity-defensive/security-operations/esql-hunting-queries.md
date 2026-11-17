---
id: computing-software.cybersecurity-defensive.security-operations.esql-hunting-queries
name: esql-hunting-queries
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [elastic, esql, threat-hunting, elastic-security, stats, enrich, detection-engineering, hunting-queries]
level: practitioner
status: docs-checked
description: "Hunt with Elastic ES|QL: piped FROM/WHERE/STATS queries for rare parents and long-tail destinations, METADATA fields, ENRICH policies, row limits and documented limitations."
sources: ["https://www.elastic.co/docs/reference/query-languages/esql", "https://www.elastic.co/docs/reference/query-languages/esql/esql-functions-operators", "https://www.elastic.co/docs/reference/query-languages/esql/limitations", "https://www.elastic.co/docs/reference/query-languages/esql/esql-metadata-fields", "https://www.elastic.co/docs/reference/query-languages/esql/esql-enrich-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ES|QL hunting queries

ES|QL is Elastic's piped query language for filtering, transforming and analysing data. Each
line is a step and the output of one step feeds the next. It runs in Kibana Discover, Dashboards,
Dev Tools and the Elastic Security and Observability analysis tools, or through the Elasticsearch
`_query` endpoint.

## Syntax essentials
Documented building blocks: `FROM` names the index or data stream, `WHERE` filters, `EVAL`
creates columns, `STATS ... BY` aggregates, `SORT`, `LIMIT`, `KEEP` selects columns,
`DISSECT` and `GROK` parse strings, `ENRICH` adds columns from an enrich policy.
Aggregate functions include `COUNT`, `COUNT_DISTINCT`, `MAX`, `MIN`, `VALUES` and `TOP`;
functions exist for date truncation (`DATE_TRUNC`), IP ranges (`CIDR_MATCH`) and lower-casing
(`TO_LOWER`). Check the function reference for exact signatures before relying on one.
```
FROM logs-endpoint.events.process-*
| STATS hosts = COUNT_DISTINCT(host.name), runs = COUNT(process.name) BY process.parent.name, process.name
| WHERE hosts <= 2
| SORT runs ASC
| LIMIT 100
```
This is a stacking (long-tail) shape: rare parent-child pairs are the leads. The index
pattern and the field names (`host.name`, `process.name`) are examples; use your own data
view's fields. Add a time filter on `@timestamp` as your deployment requires.

## Limits and behaviour (documented)
- A query returns up to 1,000 rows by default; `LIMIT` can raise it to 10,000, and queries never return more than 10,000 rows (a configurable limit). Filtering and grouping still run over all matching documents.
- Fields searched as `text` without the full-text functions (`MATCH`, `MATCH_PHRASE`, `QSTR`, `KQL`) behave as keyword fields: case-sensitive and matching the full string.
- Querying a column of an unsupported type returns an error; if unused it comes back as nulls.
- By default, referencing an unmapped field is an error.

## METADATA
`FROM index METADATA _index, _id` exposes document metadata; documented fields include `_id`,
`_index`, `_index_mode` and `_version`. Only `FROM` supports `METADATA`.

## ENRICH
Create an enrich policy (API or Kibana Index Management), execute it to build the enrich index,
then use it:
```
| ENRICH languages_policy ON a WITH name = language_name
```
(The docs' own example; `ON` names the input column, `WITH` selects enrich fields, by default all
enrich fields are added.) A created policy cannot be updated; update the source indices and
execute the policy again, which builds a new enrich index.

## Verify
Cross-check one result in Discover on the same time range and confirm the raw events match.

## Checked
Date: 2026-11-07. Read: the ES|QL reference overview, the Limitations page (row limits table, text-field and unsupported-type behaviour, unmapped fields), Metadata fields (METADATA directive, field table), Enrich data (create/execute/use steps, `ON` and `WITH` examples) and the functions/operators index (function names only). Removed as unconfirmed: the "GA in 8.14+" claim, `NOW() - 7 days`, `LIKE`/`RLIKE` examples and the encoded-PowerShell query, the beacon-regularity and rare-destination queries, `DROP`, `RENAME` and `COUNT(*)` (not seen on the pages read), multivalue-function gotchas, the high-cardinality memory warning, and the entire "From hunt to rule" section (Security rule UI steps, one-alert-per-row, `METADATA _id, _index, _version` deduplication): the Elastic rule-creation page is a stub. Individual command and function reference pages were not opened, so no function signatures are asserted.
Method: documentation only; no commands were run.
