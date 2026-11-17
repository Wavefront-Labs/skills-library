---
id: computing-software.cybersecurity-defensive.splunk.spl-stats-eventstats-streamstats
name: spl-stats-eventstats-streamstats
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, stats, eventstats, streamstats, investigation, aggregation, running-totals]
level: practitioner
status: draft
description: "Choose between stats, eventstats and streamstats in SPL investigations: aggregation, per-event context, running windows, and the memory limits of each."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Stats", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Eventstats", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Streamstats"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# stats, eventstats and streamstats

**Goal:** pick the right aggregation command so the search is correct and fast.

| Command | Output | Distributed | Use for |
|---|---|---|---|
| `stats` | one row per group, events discarded | yes, map-reduce on indexers | counts, distinct counts, summaries |
| `eventstats` | every event kept, aggregate added as a field | partly; final pass on search head | compare an event to its group (percent of total, deviation) |
| `streamstats` | every event kept, running aggregate in event order | no, search head | sequences, running windows, "first time seen", gaps |

## Patterns
Percent of a user's activity per host (eventstats keeps the events):
```
index=auth action=success | stats count by user, dest
| eventstats sum(count) as user_total by user
| eval pct=round(100*count/user_total,1) | where pct<2
```
Failed-then-success (brute force that worked) with streamstats over a sliding window:
```
index=auth (action=failure OR action=success) | sort 0 user _time
| streamstats time_window=10m count(eval(action="failure")) as fails by user
| where action="success" AND fails>=10
```
Time since previous event per host (gap detection):
```
... | sort 0 host _time | streamstats current=f last(_time) as prev by host
| eval gap=_time-prev | where gap>3600
```
Running count reset per group: `streamstats count as n reset_on_change=true by session_id`.

## Performance rules
- Reduce before you widen: filter in the base search, `stats` early, then `eventstats`
  over the smaller result.
- `eventstats` and `streamstats` hold data in search head memory (`max_mem_usage_mb` in
  limits.conf); on millions of raw events they truncate or spill. Pre-aggregate with
  `stats` or `tstats` first.
- `streamstats` processes events in the order they arrive (reverse time by default).
  `sort 0 _time` first when order matters; `sort` without `0` truncates at 10,000.
- `time_window` requires events sorted by time and works only with a `by` clause when
  input is sorted by `_time`.
- `dc()` is exact in `stats`; `estdc()` is faster and approximate.

## Verify
Run the search with a small known dataset (`| makeresults count=20 | streamevals...` or a
sandbox index) and confirm counts by hand before scheduling it as a detection.
