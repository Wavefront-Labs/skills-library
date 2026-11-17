---
id: computing-software.cybersecurity-defensive.splunk.spl-subsearch-and-join-alternatives
name: spl-subsearch-and-join-alternatives
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, subsearch, join-command, append, search-performance, investigation, format-command]
level: advanced
status: draft
description: "Use SPL subsearches safely and replace join with stats or lookups: subsearch limits, format output, and the patterns that scale."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Search/Aboutsubsearches", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Join", "https://docs.splunk.com/Documentation/Splunk/latest/Search/Abouteventcorrelation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subsearches and join alternatives

**Goal:** correlate two datasets without hitting silent subsearch limits.

## How a subsearch works
The bracketed search runs first and its results are rendered as a search string:
```
index=proxy [ search index=threat_intel type=domain | fields dest_host ]
```
becomes `index=proxy ( (dest_host="evil.example") OR (dest_host="bad.example") ... )`.
Check the rendered string by running the inner search with `| format` appended.

Defaults (limits.conf `[subsearch]`): `maxout = 10000` results, `maxtime = 60` seconds.
Beyond either, the subsearch is truncated **silently** (a small warning in the job
inspector), so the outer search misses data.

## Good subsearch uses
- Small, bounded inner results: list of compromised hosts, one user's IPs.
- Time bounding: `index=edr [ search index=alerts id=123 | eval earliest=_time-3600, latest=_time+3600 | fields earliest latest host ]`.
- Return a single value: `| return 1 $user` or `| return user`.

## join and why to avoid it
`join` is a subsearch too (50,000 row limit, 60 s timeout by default) and runs on the
search head. Replace with:

**stats over both datasets** (the default answer):
```
(index=dhcp sourcetype=dhcp) OR (index=proxy)
| eval ip=coalesce(assigned_ip, src_ip)
| stats values(hostname) as hostname values(url) as url by ip
```
**lookup** when one side is a reference table (assets, users).
**append + stats** when the two searches need different commands:
```
| tstats count as proxy_hits where index=proxy by src_ip
| append [ | tstats count as edr_events where index=edr by src_ip ]
| stats sum(*) as * by src_ip
```

## Gotchas
- The inner search runs over the time range of the outer search unless overridden.
- Field names returned by the subsearch must match fields in the outer events exactly
  (rename inside the subsearch).
- `NOT [ subsearch ]` with a truncated inner result produces false positives, the worst
  failure for an allowlist.

## Verify
Open the job inspector (Job > Inspect Job) and confirm no "subsearch truncated" or
"maxout" messages; compare counts with a stats-based version of the same correlation.
