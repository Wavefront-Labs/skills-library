---
id: computing-software.cybersecurity-defensive.security-operations.anomaly-based-detections
name: anomaly-based-detections
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-engineering, anomaly-based-detection, baselining, first-seen, statistical-detection, peer-group, behavioural-detection]
level: advanced
status: draft
description: "Build behavioural detections that work: first-seen and rare-value logic, per-entity baselines with stdev or MAD, peer groups, seasonality, and controlling false positives."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Anomalydetection", "https://learn.microsoft.com/en-us/kusto/query/series-decompose-anomalies-function", "https://www.elastic.co/guide/en/security/current/machine-learning.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anomaly-based behavioural detections

Signatures catch known bad; anomalies catch "unusual for this entity". Most anomaly rules fail
because unusual is common. Constrain them hard.

## Patterns that work
1. **First seen** (per entity, with a learning window): new admin tool on a server, user logging
   in from a new country, new process making outbound connections. Keep a lookup of seen pairs.
   ```
   index=edr event=network process!="" | stats earliest(_time) as first by host process
   | where first > relative_time(now(),"-1d")     ``` against a 30-day history lookup ```
   ```
2. **Rare across the population**: value seen on <= N hosts (stack counting as a rule).
3. **Volume deviation per entity**: bytes out, failed logons, file deletions vs that entity's
   own baseline.
   ```kql
   DeviceNetworkEvents
   | summarize bytes=sum(SentBytes) by DeviceName, bin(Timestamp, 1h)
   | make-series b=sum(bytes) default=0 on Timestamp step 1h by DeviceName
   | extend (anoms, score, base) = series_decompose_anomalies(b, 3.0)
   ```
4. **Peer group deviation**: user accessing far more files/repos than colleagues in the same role.

## Statistics choices
- Mean + 3 stdev breaks on skewed data (one huge spike inflates the stdev). Median + k x MAD is
  more robust.
- Account for seasonality (weekday/weekend, month-end): compare to the same hour-of-week, or use
  decomposition functions.
- Minimum absolute thresholds: "5x baseline" of 2 events is 10 events, not an incident.

## Controlling noise
- Scope to high-value entities (admins, servers, crown-jewel data) first.
- Combine anomalies with a second condition (anomaly AND sensitive asset, anomaly AND new process).
- Send anomalies to risk scoring (RBA) rather than straight to analysts.
- Exclude known change windows and onboarding (new users have no baseline).

## Platform options
Splunk (`anomalydetection`, MLTK, ES UBA), Sentinel (UEBA, anomaly rules, KQL series functions),
Elastic ML jobs (prebuilt security jobs: rare process, unusual login times).

## Gotchas
- Baselines learned during a compromise treat attacker behaviour as normal; use a clean period.
- Long baseline windows are expensive; precompute with summary indexes or scheduled tables.

## Verify
Backtest 30 days: alert volume per day, and inject a synthetic anomaly (replayed data) to confirm
it fires; review the top 20 alerts for precision before enabling.
