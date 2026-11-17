---
id: computing-software.cybersecurity-defensive.system-hardening.log-volume-estimation
name: log-volume-estimation
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [log-volume-estimation, eps, siem-sizing, log-management, storage-planning, licensing]
level: practitioner
status: draft
description: "Estimate log volume for SIEM and log platforms: events per second and GB/day per source type, measuring samples, peak factors, compression, retention storage and cost levers."
sources: ["https://csrc.nist.gov/pubs/sp/800/92/final", "https://docs.splunk.com/Documentation/Splunk/latest/Capacity/Estimateyourstoragerequirements", "https://learn.microsoft.com/en-us/azure/sentinel/billing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log volume estimation

SIEM licences and storage are priced by ingest volume (GB/day) or events per second (EPS). Bad estimates lead
to either surprise bills or dropping the logs you need. Measure, don't guess.

## 1. Inventory sources
List source types and counts: domain controllers, Windows servers, workstations, Linux servers, firewalls,
proxies, DNS, EDR telemetry, cloud audit logs (CloudTrail, Entra ID, M365), SaaS, applications, network flow.

## 2. Measure samples
For each type, measure a representative device over at least a week (business cycles matter):
- Windows: size and record counts of exported event logs, or forwarder throughput metrics.
- Linux/syslog: `du` of rotated logs per day; `wc -l` for events.
- Firewalls/proxies: vendor log statistics or syslog collector counters.
- Cloud: provider usage reports (CloudTrail event counts, Log Analytics `Usage` table, `_BilledSize`).
- If already in a SIEM: Splunk `index=_internal source=*license_usage.log type=Usage | stats sum(b) by st`,
  Sentinel `Usage | summarize sum(Quantity) by DataType`.

## 3. Compute
`daily GB = sum(devices x avg bytes/event x events/day)`; `EPS = events/day / 86400`.
Typical orders of magnitude vary hugely by audit policy, so treat any rule-of-thumb only as a sanity check:
domain controllers and perimeter firewalls/proxies are usually the largest per device; EDR raw telemetry can
dwarf everything else.
Apply a **peak factor** (2-3x average) for EPS sizing (morning logons, incidents, scans) and **growth** (20-30%
per year).

## 4. Storage
- Hot/searchable: `daily GB x hot days x (index overhead or compression ratio)`. Splunk rule of thumb: about
  50% of raw size on disk (compressed rawdata ~15% plus index files ~35%), validated per data type; replication
  factor multiplies it.
- Cold/archive: compressed object storage, often 5-10x smaller than raw, for long retention requirements.

## 5. Cost levers (without blinding yourself)
- Filter noise at source (verbose debug logs, health checks, successful 4663 object access on high-churn
  shares), but keep security-relevant events identified in detection use cases.
- Route by value: high-value security logs to the SIEM analytics tier, bulk/verbose logs to cheaper tiers
  (Sentinel basic/auxiliary logs, Splunk federated search to S3, data lake).
- Summarise flows/metrics instead of raw where detection allows.
- Re-measure after every audit policy change.

## Verify
Estimate within about 20% of actual ingest after the first month; dashboards track daily volume per source type
with alerts on sudden drops (logging broke) or spikes (misconfiguration or attack).
