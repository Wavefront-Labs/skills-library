---
id: computing-software.digital-forensics-incident-response.log-analysis.siem-query-performance-optimisation
name: siem-query-performance-optimisation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [query-optimization, kql, spl, siem-performance, threat-hunting, dfir]
level: practitioner
status: draft
description: "Make SIEM hunting queries fast and reliable in KQL, SPL and Elastic: time and index filters first, indexed fields, has vs contains, tstats/summary data, join order and truncation traps."
sources: ["https://learn.microsoft.com/en-us/kusto/query/best-practices", "https://docs.splunk.com/Documentation/Splunk/latest/Search/Writebettersearches", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Tstats", "https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SIEM query performance optimisation

During incidents, slow queries mean fewer hypotheses tested, and timed-out or truncated queries produce false negatives. Optimisation is about correctness as much as speed.

## Universal rules
1. **Time first**: narrowest time range that answers the question.
2. **Narrow the source**: specific table/index/sourcetype, not `*`.
3. **Filter early on indexed or cheap fields** (exact match on keyword fields, event IDs) before string scans or parsing.
4. **Aggregate before joining**; join small to large.
5. **Project only needed columns** before heavy operations.
6. **Know the row/result limits** and check whether results were truncated.

## KQL (Sentinel / Defender / Log Analytics)
- `where TimeGenerated > ago(1d)` first; then `where EventID == 4624`.
- `has` (term index) beats `contains` (substring scan); `has_any` for lists; `==` beats `=~`.
- Avoid `parse`/`extract` on all rows; filter first.
- `summarize` before `join`; put the smaller table on the left; use `join kind=inner` hints (`hint.strategy=shuffle` for large keys).
- `materialize()` reused subqueries; `lookup` for small dimension tables.
- Advanced hunting caps results (e.g. 100,000 rows displayed) and query time; split by time if needed.

## SPL (Splunk)
- `index=wineventlog sourcetype=XmlWinEventLog EventCode=4688` at the start; avoid leading wildcards (`*mimikatz*` forces full scans; prefer `TERM()` or field extractions at index time).
- `tstats` over accelerated data models (`| tstats count from datamodel=Endpoint.Processes where Processes.process_name=rundll32.exe by Processes.dest`) is orders of magnitude faster than raw search.
- `fields` early; `stats` instead of `transaction`; avoid `join` (subsearch limits of 50,000 results / 60 s by default truncate silently); use `stats` by common key instead.
- Job Inspector shows where time is spent.

## Elastic
- Filter context (`filter` clauses, `WHERE` on keyword) is cached and faster than scoring queries; use `keyword` fields for exact match.
- Avoid leading wildcards and regex on high-cardinality text; use runtime fields sparingly.
- Narrow index patterns; ES|QL `LIMIT` and Discover sample sizes cap results.

## Gotchas
- A "no results" answer from a query that hit a limit or timed out is not evidence of absence; record the query, time range and completion status.
- Saved hunts degrade as data grows; re-check runtime periodically.

## Verify
Optimised and original queries return the same result counts on a sample window, and the hunt record notes any limits encountered.
