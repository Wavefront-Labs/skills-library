---
id: computing-software.cybersecurity-defensive.splunk.spl-detection-searches
name: spl-detection-searches
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, splunk-enterprise-security, detection-engineering, saved-searches, savedsearches-conf, correlation-search, tstats, data-models, cim, common-information-model, throttling, alert-suppression, risk-based-alerting, rba, kql, microsoft-sentinel, elastic-security, eql, esql, sigma, siem, detection-as-code, lookups]
level: practitioner
status: draft
description: "Write SPL detections that are fast (tstats on CIM data models), scheduled safely as saved-search alerts, throttled, tested and portable to KQL/Elastic."
sources: ["Splunk Docs - Search Reference (tstats, stats, lookup)", "Splunk Docs - Common Information Model Add-on Manual", "Splunk Docs - Configure scheduled reports and alert throttling (savedsearches.conf)", "Splunk Security Content (research.splunk.com) detection library", "MITRE ATT&CK Enterprise matrix"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPL detection searches — alerts that fire on behaviour, not on noise

**Goal:** turn a detection idea into a scheduled Splunk search that runs cheaply, fires
once per real incident, carries enough context to triage, and can be ported to
Sentinel or Elastic without a rewrite from scratch.

## 1. Start from the hypothesis and the data
Write one line: *"Alert when <actor> does <behaviour> on <asset> that baseline says is rare."*
Map it to an ATT&CK technique ID. Then confirm the data exists and is normalised:
```
| tstats count where datamodel=Endpoint.Processes by Processes.dest span=1d
```
If that returns nothing, the source isn't CIM-mapped (missing TA, wrong sourcetype,
data model not accelerated). Fix that first — a detection on unmapped raw data
breaks the next time the vendor changes a field name.

## 2. Prefer tstats over raw search
`tstats` reads accelerated data model summaries (tsidx), often 10–100x faster than
`index=... | stats`. Pattern:
```
| tstats summariesonly=true allow_old_summaries=true count min(_time) as firstTime max(_time) as lastTime
  from datamodel=Endpoint.Processes
  where Processes.parent_process_name IN ("winword.exe","excel.exe","outlook.exe")
        Processes.process_name IN ("powershell.exe","cmd.exe","wscript.exe","mshta.exe")
  by Processes.dest Processes.user Processes.parent_process_name Processes.process_name Processes.process
| `drop_dm_object_name(Processes)`
| convert ctime(firstTime) ctime(lastTime)
| lookup asset_lookup_by_str dest OUTPUT priority as dest_priority
| where NOT match(process, "(?i)known-addin-path")
```
- `summariesonly=true` ignores unsummarised (recent/unaccelerated) events — fast, but
  you can miss the last few minutes. Leave a lag (see 3).
- Filter in the `where` clause of tstats, not after — post-filters scan everything.
- Raw `index=` searches are fine for low-volume sources; always name `index` and
  `sourcetype`, and avoid leading wildcards (`*foo`) which defeat the index.

## 3. Schedule it as an alert (savedsearches.conf)
```
[Office App Spawning Shell]
search = <the SPL above>
cron_schedule = */15 * * * *
dispatch.earliest_time = -20m@m
dispatch.latest_time = -5m@m
schedule_window = auto
enableSched = 1
counttype = number of events
relation = greater than
quantity = 0
alert.suppress = 1
alert.suppress.fields = dest,process_name
alert.suppress.period = 4h
action.notable = 1
```
(`action.notable` is Enterprise Security; elsewhere use `action.email` or `action.webhook`.
Splunk .conf files do not support inline comments — put comments on their own line.)
- Overlap the window slightly (20 min lookback, 15 min schedule) and end it at `-5m`
  so late-indexed events still land in a run. Track duplicates with throttling, not
  by shrinking the window.
- Throttle on the entity fields (`dest`, `user`) so one host spraying 300 events is
  one alert, but a second host still fires.
- In Enterprise Security, consider Risk-Based Alerting: emit a risk score per entity
  (`action.risk`) and alert on the aggregate (e.g. risk over a threshold across 3+
  distinct ATT&CK tactics in 24 h). Thresholds are environment-specific — tune them.

## 4. Test before enabling
1. Run over 30 days of history; count hits per day and per entity. Over ~5/day for a
   single analyst queue means you need allowlisting or RBA, not a notable.
2. Replay a true positive (Atomic Red Team test in a lab, or an attack-data sample)
   and confirm it fires.
3. Check cost: Job Inspector → `scanCount`, run duration. A 15-minute schedule
   that takes 10 minutes will skip runs.
4. Keep allowlists in a lookup (`| lookup detection_allowlist ...`), not hard-coded
   in the SPL, and give each entry an owner and expiry date.

## 5. Port to other SIEMs
- **KQL (Microsoft Sentinel):** `DeviceProcessEvents | where InitiatingProcessFileName in~ ("winword.exe") and FileName in~ ("powershell.exe") | summarize count(), min(Timestamp) by DeviceName, AccountName` as a Scheduled analytics rule with entity mapping and grouping/suppression.
- **Elastic Security:** EQL `process where process.parent.name : "winword.exe" and process.name : "powershell.exe"` in a detection rule, ECS fields, alert suppression by `host.name`.
- Store the canonical logic as Sigma in Git and convert with pySigma backends; review
  the output — converters handle field mapping, not performance.

## Gotchas
- An unaccelerated or rebuilding data model makes `summariesonly=true` return zero
  silently. Monitor acceleration status, and alert when a detection's source volume drops.
- `_time` is event time; late or clock-skewed sources fall outside your window. Compare
  `_indextime - _time` for each source.
- `IN`/`match` are case-sensitive on some field types; normalise with `lower()`.
- Skipped searches (scheduler concurrency limits) are a silent detection gap — watch
  `index=_internal sourcetype=scheduler status=skipped`.
- Throttle fields that don't exist in the results suppress nothing.

## Verify
- [ ] The search uses CIM field names and returns data via `tstats` for the target data model.
- [ ] Window overlaps the schedule and ends a few minutes before now.
- [ ] Throttling is keyed on entity fields that appear in the output.
- [ ] A replayed true positive fires exactly one alert.
- [ ] 30-day backtest volume is within the queue's capacity.
- [ ] No skipped runs in the scheduler log over a week.

Related: computing-software.cybersecurity-defensive.security-operations.alert-triage,
computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling
