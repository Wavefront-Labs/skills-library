---
id: computing-software.cybersecurity-defensive.splunk.log-source-health-monitoring
name: log-source-health-monitoring
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, log-source-health, silent-log-loss, tstats, data-source-monitoring, missing-hosts, ingest-latency, meta-woot]
level: practitioner
status: draft
description: "Detect silent log loss in Splunk: per-source baselines with tstats, missing-host alerts, ingest latency and volume-drop checks that page before a detection goes blind."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Tstats", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Metadata", "https://splunkbase.splunk.com/app/2949"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log source health and silent log loss

**Goal:** know within an hour when a host, sourcetype or whole feed stops sending, slows
down or drops volume. Detections over missing data return zero results and look healthy.

## 1. Inventory expected sources
Keep a lookup `expected_sources.csv` with `index, sourcetype, host_pattern, owner,
max_gap_minutes, criticality`. Seed it from what is currently arriving:
```
| tstats latest(_time) as last count where index=* earliest=-7d by index sourcetype
| eval last_seen=strftime(last,"%F %T")
```

## 2. Feed-level silence
```
| tstats latest(_time) as last where index=* earliest=-24h by index sourcetype
| inputlookup append=t expected_sources.csv
| stats max(last) as last values(max_gap_minutes) as gap values(owner) as owner by index sourcetype
| eval mins_silent=round((now()-last)/60) | where isnull(last) OR mins_silent > gap
```
Schedule every 15 minutes; route to the owning team, not only the SOC.

## 3. Host-level dropouts
```
| tstats latest(_time) as last where index=wineventlog earliest=-7d by host
| where last < relative_time(now(),"-4h")
```
Join against the asset inventory or AD to exclude decommissioned hosts. Domain controllers
and crown-jewel servers get a tighter threshold.

## 4. Volume drops (partial loss)
```
| tstats count where index=firewall earliest=-15d@h latest=@h by _time span=1h
| eval hour=strftime(_time,"%H"), dow=strftime(_time,"%a")
| eventstats median(count) as med by hour dow
| where _time >= relative_time(now(),"-1h@h") AND count < 0.5*med
```
A firewall that drops from 40k to 4k events per hour is broken even though it is "sending".

## 5. Latency
```
| tstats max(_indextime) as it min(_time) as t where index=* earliest=-1h by index sourcetype
```
Prefer computing `_indextime - _time` on raw events for the top sources; latency over a few
minutes breaks real-time detections with short lookbacks.

## Gotchas
- `metadata` and `tstats` respect your role's index access; run health searches as a role
  that can see everything.
- Clock skew on sources makes events look late or early; check `lag` before blaming transport.
- Forwarder-level health is in `index=_internal sourcetype=splunkd group=tcpin_connections`.
- Free option: Splunkbase "Meta Woot!" or TrackMe apps do this out of the box.

## Verify
Stop a test forwarder or block a syslog source for longer than its `max_gap_minutes`; the
alert must fire and reach the owner.
