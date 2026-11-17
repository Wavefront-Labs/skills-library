---
id: computing-software.cybersecurity-defensive.threat-intelligence.ioc-retro-hunting
name: ioc-retro-hunting
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [iocs, retro-hunting, historical-ioc-search, threat-intel-matching, lookback, ioc-sweep, siem]
level: practitioner
status: draft
description: "Search historical logs for newly published IOCs: lookback windows by indicator type, scheduled retro-match jobs, handling hits from before the IOC was known, and reporting."
sources: ["https://www.cisa.gov/news-events/cybersecurity-advisories", "https://learn.microsoft.com/en-us/azure/sentinel/use-matching-analytics-to-detect-threats", "https://docs.splunk.com/Documentation/ES/latest/Admin/Addthreatintelligence"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOC retro-hunting

Real-time matching only catches indicators seen after the IOC entered your platform. Intrusions are
usually reported weeks to months after the activity, so every new high-confidence IOC set needs a
lookback search.

## When
- New CISA/vendor advisory or ISAC report relevant to your sector or technology stack.
- New IOCs from your own incidents (search the whole estate, not just the affected host).
- High-confidence feed additions (scheduled job).

## Lookback windows (match to retention and indicator lifetime)
| Indicator | Typical lookback |
|---|---|
| File hashes | As far as retention allows (hashes do not "expire") |
| Domains | Back to domain registration date or first-seen in passive DNS |
| IPs | Days to weeks around the reported activity window (IPs get reassigned) |
| URLs, user agents, JA4 | Report's activity window plus margin |

## Execution
- SIEM: scheduled search joining the IOC lookup against summarised tables (DNS, proxy, firewall, EDR
  process/file events), e.g. Splunk `| tstats ... where [| inputlookup new_iocs.csv | fields dest]` or
  Sentinel query with `materialize()` of the indicator list over 90 days.
- Cold data: search archived logs (Sentinel Search jobs/restore, Splunk frozen archives, S3/Athena,
  Elastic searchable snapshots) for high-severity IOC sets.
- EDR: hash and filename hunts across endpoints (historical telemetry window of the EDR, often 30-180 days).
- Email: message trace/historical search for sender domains and subjects.

## Handling hits
- A hit predating the IOC publication is not automatically a compromise: check context (was the IP a CDN
  then? did the host resolve the domain via ad traffic?), but treat as a potential incident until cleared.
- Record negative results with the time range and sources searched: leadership asks "were we affected?"
  and the answer must state coverage and gaps.

## Automation
Scheduled job per new TIP event above a confidence threshold, with results written back as sightings
(MISP) or comments so analysts know where indicators were (not) seen.

## Gotchas
- Retention shorter than the threat's dwell time makes "no hits" weak evidence; say so.
- IOC sets from advisories include defanged values (`hxxp`, `[.]`): normalise before matching.

## Verify
Seed a known historic value (e.g. an internal test domain resolved 60 days ago) into the IOC list and confirm
the retro job finds it in the correct data sources.
