---
id: computing-software.digital-forensics-incident-response.log-analysis.baselining-normal-to-find-anomalies
name: baselining-normal-to-find-anomalies
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [baselining, anomaly-detection, threat-hunting, behavioural-baseline, ueba, kql, splunk, dfir]
level: practitioner
status: draft
description: "Build behavioural baselines of logons, processes, network and admin activity, then hunt deviations: time windows, peer groups, thresholds and false-positive control."
sources: ["https://www.sans.org/white-papers/", "https://learn.microsoft.com/en-us/kusto/query/series-decompose-anomalies-function", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Anomalydetection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Baselining normal to find anomalies

**Goal:** know what normal looks like for an account, host or peer group, so deviations stand
out during hunts and incidents.

## What to baseline
| Entity | Baseline features |
|---|---|
| User accounts | logon hours, source hosts/IPs/countries, logon types, MFA methods, apps used |
| Admin/service accounts | hosts they log on to, tools they run, times; service accounts should be extremely regular |
| Hosts | parent-child process pairs, listening ports, outbound destinations, data volumes |
| Network | bytes per host per hour, protocols per segment, DNS query volume, new domains per day |
| Cloud | API calls per principal, regions used, resource creation rate |

## Building the baseline
1. Choose a lookback (typically 14-30 days) free of known incidents; exclude the incident window
   when baselining during response.
2. Aggregate per entity and time bucket (hour of week captures weekday/weekend patterns).
3. Store as a lookup/watchlist (Splunk lookup, Sentinel watchlist, Elastic transform) and refresh
   on a schedule.

## Detecting deviations
```kusto
// First time a user logs on to a given host in 30 days
let baseline = SecurityEvent
| where TimeGenerated between (ago(31d) .. ago(1d)) and EventID == 4624
| distinct Account, Computer;
SecurityEvent
| where TimeGenerated > ago(1d) and EventID == 4624 and LogonType in (3, 10)
| join kind=leftanti baseline on Account, Computer
```
```kusto
// Time-series anomalies in outbound bytes per device
DeviceNetworkEvents | make-series Bytes = count() default=0 on Timestamp from ago(14d) to now() step 1h by DeviceName
| extend (anomalies, score, baseline) = series_decompose_anomalies(Bytes, 3)
```
- First-seen logic (new process/hash/destination for this host or peer group) is simple and
  effective.
- Statistical thresholds (mean + 3 sigma, percentiles) for volumes; peer-group comparison (user
  vs others in the same department/role).

## Controlling noise
- Seasonality: month-end processing, patch Tuesdays, backup windows.
- Organisational change: new projects, migrations, travel; liaise with IT before escalating.
- Rank deviations by risk (privileged account, sensitive host) rather than alerting on all.

## During incident response
Baselines answer "is this normal for this account?" quickly, e.g. whether a service account's
interactive logon or an admin's 03:00 RDP session is unprecedented.

## Self-check
Each baseline states its lookback, entity grouping and refresh cadence, and each flagged
deviation was checked against known business events.
