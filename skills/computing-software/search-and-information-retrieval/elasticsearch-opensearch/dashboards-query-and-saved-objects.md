---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.dashboards-query-and-saved-objects
name: dashboards-query-and-saved-objects
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, dashboards-query-and-saved-objects]
level: practitioner
status: docs-checked
description: "Search data in Dashboards with DQL/Lucene, create index patterns and export saved objects for backup."
sources:
  - https://docs.opensearch.org/latest/dashboards/dql/
  - https://docs.opensearch.org/latest/dashboards/management/index-patterns/
  - https://docs.opensearch.org/latest/dashboards/management/saved-objects/
  - https://docs.opensearch.org/latest/dashboards/management/management-index/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dashboards queries and saved object backup

**Goal:** reproducible dashboards.
- OpenSearch Dashboards uses DQL by default; switch to Lucene (query string query) with the language toggle next to the search box. DQL supports `and`, `or` and `not` (case-insensitive) and `*` wildcards in terms and field names, e.g. `status:500 and host:web*`.
- When creating an index pattern, pick the date field to use for time filtering in the Time field list (e.g. `@timestamp`); it cannot be changed after the pattern is created, so create a new pattern to use another field.
- Export saved objects from Stack Management > Saved objects (tick Include related objects so references come along); the file is NDJSON, one object per line plus a summary line. Keep it in version control and import it into another instance.
- Import options: "Create new objects with unique IDs" imports copies; "Check for existing objects" plus "Automatically overwrite conflicts" or "Request action on conflict" handles id clashes.
- Multi-tenancy imports into the current tenant, so switch to the target tenant first. A single import or export is limited to 10,000 objects and 25 MB.
- The same NDJSON works with the Saved Objects APIs; the API path was not checked here.
- Failure mode: importing without a conflict option can clash with existing ids.

## Verify
- [ ] The exported NDJSON imports into a clean Dashboards instance and the dashboard renders.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited pages are OpenSearch Dashboards; Kibana was not checked here.

## Checked
2026-11-08. Read the OpenSearch Dashboards DQL, Index patterns, Saved objects and Stack Management pages (the Saved objects page in part, via targeted search). Confirmed DQL default and Lucene toggle, operators, wildcards, time field selection and immutability, NDJSON export, import options, tenant behaviour and limits. Removed "wrong time field shows empty Discover" and the `/api/saved_objects` path (not confirmed on pages read).
Method: documentation only; no commands were run.
