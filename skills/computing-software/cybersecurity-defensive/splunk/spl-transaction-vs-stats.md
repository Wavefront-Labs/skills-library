---
id: computing-software.cybersecurity-defensive.splunk.spl-transaction-vs-stats
name: spl-transaction-vs-stats
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, transaction-command, stats, session-grouping, investigation, maxspan, search-performance]
level: practitioner
status: draft
description: "Group related events in SPL: when the transaction command is worth its cost, and how to get the same sessions faster with stats and streamstats."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Transaction", "https://docs.splunk.com/Documentation/Splunk/latest/Search/Abouttransactions", "https://docs.splunk.com/Documentation/Splunk/latest/Search/Abouteventcorrelation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grouping events: transaction vs stats

**Goal:** stitch events into sessions (logon to logoff, VPN connect to disconnect, mail
flow by message ID) correctly without killing the search head.

## transaction: what it gives you
```
index=vpn | transaction user startswith="action=connect" endswith="action=disconnect" maxspan=12h maxpause=1h keepevicted=true
| eval duration_min=round(duration/60) | table user _time duration_min eventcount closed_txn
```
- Adds `duration`, `eventcount`, `closed_txn`, and keeps raw events together (handy for
  reading a session as a story).
- `startswith`/`endswith` and `maxpause` express ordering logic stats cannot easily.
- `keepevicted=true` plus `closed_txn=0` finds sessions that never ended.

## Costs
- Runs entirely on the search head, after all events are returned. Memory limits
  (`maxopentxn`, `maxopenevents` in limits.conf) evict transactions silently on big data,
  so results are incomplete without an error.
- Not usable in data model acceleration or tstats.

## stats equivalent (preferred when a shared key exists)
```
index=vpn (action=connect OR action=disconnect)
| stats min(_time) as start max(_time) as end values(src_ip) as src count by user session_id
| eval duration_min=round((end-start)/60)
```
Ten to a hundred times faster because indexers pre-aggregate. Use `values()`/`list()` to
keep the details you need.

No session ID? Build one with streamstats, then stats:
```
index=vpn | sort 0 user _time
| streamstats current=f last(_time) as prev by user
| eval new=if(isnull(prev) OR _time-prev>3600,1,0)
| streamstats sum(new) as sess by user
| stats min(_time) as start max(_time) as end count by user sess
```

## Decision rule
- Shared unique ID (message ID, session ID, request ID): `stats`.
- Inactivity gap defines the session: streamstats then stats.
- Ordered start/end markers with unclear keys, small time range, interactive analysis:
  `transaction` is fine.

## Verify
Run both forms over the same hour and compare session counts; a mismatch usually means
transaction evicted sessions or the stats key is not unique.
