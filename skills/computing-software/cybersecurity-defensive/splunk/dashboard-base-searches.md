---
id: computing-software.cybersecurity-defensive.splunk.dashboard-base-searches
name: dashboard-base-searches
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, siem-dashboards, base-search, post-process, ds-chain, chained-search, dashboard-performance, search-concurrency]
level: practitioner
status: draft
description: "Use base searches and post-processing (ds.chain / Simple XML base) so one search feeds many dashboard panels without hitting concurrency limits."
sources: ["Splunk Docs - Dashboard Studio (Chain searches together with a base search)", "Splunk Docs - Simple XML Reference (Post-process searches)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Base searches and chained searches

**Goal:** a dashboard with ten panels runs one or two searches, not ten, so it loads fast
and does not consume the search head concurrency budget.

## Pattern
Base search returns a compact transformed table; each panel post-processes it.

Dashboard Studio:
```json
"dataSources": {
  "ds_base": {"type": "ds.search", "options": {"query":
    "index=proxy sourcetype=zscaler | stats count sum(bytes_out) as bytes_out by user category action"}},
  "ds_blocked": {"type": "ds.chain", "options": {"extend": "ds_base",
    "query": "| where action=\"blocked\" | stats sum(count) as hits by category | sort - hits"}},
  "ds_top_upload": {"type": "ds.chain", "options": {"extend": "ds_base",
    "query": "| stats sum(bytes_out) as bytes by user | sort - bytes | head 10"}}
}
```
Simple XML equivalent: `<search id="base">...</search>` and `<search base="base">| where ...</search>`.

## Rules that keep it correct
1. **The base must be transforming** (`stats`, `chart`, `timechart`, `table` of limited
   fields). A non-transforming base search returns raw events, which are truncated at
   500,000 events for post-processing and also time out.
2. Include in the base every field any chained panel needs, at the finest grain needed.
   Post-process can aggregate up, never down.
3. Keep `_time` in the base (e.g. `bin _time span=1h` then `stats ... by _time ...`) if any
   panel is a time chart.
4. Recompute totals with `sum(count)`, not `count`, in chained searches.

## When not to chain
- Panels on different indexes or different time ranges: separate searches or saved searches.
- Very heavy bases: make the base a scheduled `ds.savedSearch` so all viewers share
  one cached result.

## Gotchas
- A chained search fails silently to "No results" if the base field name changes.
- Tokens used in the base re-run the whole base on every input change; tokens used only in
  the chain re-run just the post-process.
- Base search results are limited by `limits.conf` post-process limits; check for warnings in the panel.

## Verify
- [ ] Opening the dashboard creates one job per base (check Activity > Jobs).
- [ ] Panel totals match a standalone version of the same search.
