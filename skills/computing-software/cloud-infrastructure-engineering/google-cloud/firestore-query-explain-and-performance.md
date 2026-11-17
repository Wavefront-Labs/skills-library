---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firestore-query-explain-and-performance
name: firestore-query-explain-and-performance
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, firestore, firestore-query-explain, query-performance, composite-indexes, key-visualizer]
level: practitioner
status: docs-checked
description: "Diagnose slow or costly Firestore queries with Query Explain and Analyze, fix index use, and avoid hotspots from sequential IDs and the 500/50/5 ramp-up rule."
sources: ["https://github.com/googleapis/googleapis/blob/master/google/firestore/v1/query_profile.proto", "https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-firestore/google/cloud/firestore_v1/query_profile.py", "https://docs.cloud.google.com/firestore/docs/best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firestore Query Explain and query performance

## 1. Explain a query
Python client:
```python
from google.cloud.firestore_v1.query_profile import ExplainOptions
q = db.collection("orders").where("status", "==", "open").order_by("created", direction="DESCENDING").limit(50)
res = q.get(explain_options=ExplainOptions(analyze=True))
m = res.get_explain_metrics()
print(m.plan_summary.indexes_used)        # list of dicts describing the indexes the plan uses
print(m.execution_stats.results_returned, m.execution_stats.read_operations,
      m.execution_stats.execution_duration, m.execution_stats.debug_stats)
```
- `analyze=False` (the default) only plans the query and returns planning metrics; `analyze=True` plans and executes it, returning results plus execution metrics (`results_returned`, `read_operations`, `execution_duration`, `debug_stats`), and the query's reads are billed.
- `debug_stats` is subject to change; the API reference shows it can include `indexes_entries_scanned`, `documents_scanned` and billing details. Index entries scanned far above documents scanned or results returned points to a poor index for the filters.

## 2. Fix what it shows
- Order composite index fields to match the query's equality, range and order-by fields, and re-check the plan with Explain after each index change.
- Use `limit()` and cursors (`start_after`) for paging; an offset still retrieves the skipped documents internally and only avoids returning them to your application.
- Use `count()`, `sum()` or `avg()` aggregations instead of reading documents to compute them.
- Exempt large, unqueried fields (long strings, arrays, maps) from indexing to cut storage cost; large arrays and maps can approach the limit of 40,000 index entries per document.

## 3. Hotspots
- Monotonically increasing document IDs can cause hotspots that hurt latency: use auto-generated IDs. A sequentially increasing indexed field caps the collection's write rate at 500 writes per second; exempt the field from indexing if you do not query on it.
- New collections: start with at most 500 operations per second and spread them evenly across the key range (the **500/50/5** rule: increase traffic by 50% every 5 minutes).
- Key Visualizer for Firestore shows hot ranges by key over time.

## Gotchas
- A query needing a missing composite index fails with an error that links to create it; keep index definitions in version-controlled configuration rather than only clicking the link.
- Confirm Query Explain support for your database mode and client version in the Firestore documentation.

## Verify
- [ ] After adding the index, the scanned index entries approach the number of results returned.

## Checked
Checked 2026-10-24 against the googleapis `google/firestore/v1/query_profile.proto` (ExplainOptions, ExplainMetrics, PlanSummary, ExecutionStats and the documented `debug_stats` keys), the googleapis google-cloud-python `google-cloud-firestore` `query_profile.py`, `query.py` and `query_results.py` (`get(explain_options=...)`, `get_explain_metrics()`) and the Firestore best-practices page (docs.cloud.google.com). Wrong claim fixed: the debug stat key is `indexes_entries_scanned` (plural), not `index_entries_scanned`. Removed the sample index output, the `in` and `array-contains-any` 30-value claim, the Datastore-mode explain claim and the multiple-range-filter advice, none of which could be confirmed. The Query Explain documentation page returned 404.
Method: documentation only; no commands were run.
