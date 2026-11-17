---
id: computing-software.cybersecurity-defensive.splunk.data-onboarding-and-cim-mapping
name: data-onboarding-and-cim-mapping
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, data-onboarding, cim, common-information-model, props-conf, transforms-conf, field-extraction, sourcetype, index-design, data-models, tech-add-ons, ta, universal-forwarder, hec, retention, license-usage]
level: practitioner
status: draft
description: "Onboard a new log source into Splunk correctly: index/sourcetype design, field extraction via props/transforms, CIM mapping with a TA, and retention/licence sizing."
sources: ["Splunk Docs - Getting Data In", "Splunk Docs - Common Information Model Add-on Manual", "Splunk Docs - Managing Indexers and Clusters of Indexers (retention)", "Splunk Lantern - onboarding guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data onboarding and CIM mapping — make a new source usable on day one

**Goal:** get a new log source into Splunk so it's correctly timestamped, correctly
parsed, mapped to the Common Information Model (CIM) where a data model exists for
it, and sized for retention/licence before anyone builds a detection on top of it —
not after a detection silently breaks on a field rename.

## 1. Design the index and sourcetype before ingest
Don't dump everything into `main`. One index per major source family (or per
retention/access requirement — index is the access-control and retention boundary,
sourcetype is not). Name sourcetypes to match a vendor TA's expectation where one
exists (e.g. `aws:cloudtrail`, `MSWinEventLog`) so the Tech Add-on's field
extractions and CIM mapping apply without rework. Set retention
(`frozenTimePeriodInSecs` in `indexes.conf`) deliberately per index — default is
6 years, which quietly burns storage if left on a noisy, low-value source.

## 2. Timestamp extraction is the first thing to verify
Wrong `TIME_FORMAT`/`TIME_PREFIX` in `props.conf` silently assigns index time
instead of event time, which breaks every time-windowed search and backdates or
future-dates events. Check with:
```
index=<new_index> | head 20 | eval lag=_indextime-_time | table _time _indextime lag host
```
A consistently large or negative `lag` means timestamp parsing is wrong or the
source clock is skewed — fix before anyone relies on `_time`.

## 3. Field extraction: TA first, custom second
Install the vendor or Splunkbase Tech Add-on if one exists — it ships
`props.conf`/`transforms.conf` field extractions and often the CIM mapping
(`eventtypes.conf`/tags) already done. Only write custom `EXTRACT-`/`REPORT-`
stanzas for fields the TA doesn't cover. Validate extractions interactively first
(`rex` in a search) before committing to `transforms.conf` — a regex that works on
one sample event breaks on the next vendor log format change.

## 4. Map to CIM
If the source should feed a data model (Authentication, Network_Traffic,
Web, Endpoint.Processes, etc.), confirm the TA tags events correctly:
```
index=<new_index> | head 5 | table sourcetype, eventtype, tag
```
If `eventtype`/`tag` are empty, the CIM mapping isn't firing — check
`eventtypes.conf` search strings match your actual field values (case, exact
string). Then accelerate the relevant data model (`datamodel=... acceleration` in
Settings) and confirm with `| tstats count from datamodel=<model>` returning
nonzero. Un-accelerated or mis-tagged sources make every `tstats`-based detection
built on this skill's companion (spl-detection-searches) return silent zeros.

## 5. Size it
Check daily ingest volume (`index=_internal source=*license_usage.log* idx=<new_index>
| timechart sum(b) as bytes`) within the first week, before it's load-bearing —
licence overage and indexer storage growth are easier to fix with filtering/routing
at onboarding than after six months of history exists at full verbosity. Route
noisy, low-value fields to a summary index or drop them in `transforms.conf`
(`NullQueue`) rather than ingesting then filtering at search time, which costs full
licence and storage either way.

## Gotchas
- A Universal Forwarder with no `outputs.conf` load-balancing retries against a
  single indexer and silently queues/drops under load — check
  `splunkd.log` for `Forwarding to indexer group` warnings.
- HEC (HTTP Event Collector) tokens default to no index ACL restriction unless
  scoped — scope tokens to the indexes they should write to.
- Multiline events (stack traces, JSON) need `SHOULD_LINEMERGE`/`LINE_BREAKER` set
  correctly or one logical event splits into many, breaking counts and correlation.
- Clock skew on the source host is invisible until you check `_indextime - _time`;
  don't assume NTP is working.

## Verify
- [ ] `_time` matches the real event time (lag check run, not assumed).
- [ ] Extracted fields appear correctly in `| table` for a sample of real events,
      not just one log line.
- [ ] CIM tags/eventtypes populate and the relevant data model returns data via `tstats`.
- [ ] Daily licence volume was checked within the first week of onboarding.
- [ ] Retention is set deliberately for the index, not left at default.

Related: computing-software.cybersecurity-defensive.splunk.spl-detection-searches,
computing-software.cybersecurity-defensive.security-operations.alert-triage
