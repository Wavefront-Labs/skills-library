---
id: computing-software.digital-forensics-incident-response.log-analysis.log-normalisation-and-timestamp-alignment
name: log-normalisation-and-timestamp-alignment
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [log-normalization, timestamp-alignment, time-zones, clock-skew, ecs, ocsf, timeline, dfir]
level: practitioner
status: draft
description: "Normalise heterogeneous logs to one schema and UTC, detect and correct clock skew, and align sources so cross-system timelines are trustworthy."
sources: ["https://www.elastic.co/guide/en/ecs/current/index.html", "https://schema.ocsf.io/", "https://datatracker.ietf.org/doc/html/rfc3339"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log normalisation and timestamp alignment

**Goal:** merge Windows, Linux, network, cloud and application logs into one timeline where
the same moment has the same timestamp and the same field means the same thing.

## Timestamps
1. **Know each source's native format and zone:**
   - Windows EVTX: UTC (FILETIME); viewers display local time.
   - Linux syslog (RFC 3164): local time, **no year, no zone**; journald stores UTC
     microseconds.
   - IIS W3C logs: UTC by default; Apache/nginx: local time with offset (`[16/Oct/2026:09:12:01 +0100]`).
   - Cloud audit logs (CloudTrail, Entra ID, M365, GCP): UTC ISO 8601.
   - FAT/exFAT, some appliances, many firewalls: local device time.
   - Epoch variants: Unix seconds/ms, Windows FILETIME (100 ns since 1601), Mac absolute (2001),
     WebKit/Chrome (microseconds since 1601).
2. **Convert to UTC ISO 8601 / RFC 3339** with explicit zone (`2026-10-16T09:12:01.123Z`) and keep
   the original value in a separate field.
3. **Fix missing years** (RFC 3164) using file mtime and rollover order; beware December/January
   boundaries.
4. **DST:** convert with a time-zone database (IANA name like `Europe/London`), not a fixed
   offset, so the DST transition hour is handled.

## Clock skew
- Measure offset per host: compare an event seen by two systems (a Kerberos ticket request in
  DC logs vs client logs, a firewall connection vs Sysmon Event 3, a proxy request vs browser
  history). Windows records time changes as Security 4616 and System Event 1 (Kernel-General);
  W32Time events show sync failures.
- Record skew per source (e.g. "Host WS042 clock is 3 min 12 s ahead") and either correct during
  normalisation (add a corrected field) or annotate the timeline. Never silently alter originals.

## Field normalisation
- Map to a common schema: Elastic Common Schema (`source.ip`, `user.name`, `process.command_line`,
  `event.action`), OCSF, or Splunk CIM. Consistency matters more than which one.
- Normalise usernames (`DOMAIN\user`, `user@domain`, SID), hostnames (FQDN vs short, case), IPs
  (IPv4-mapped IPv6 `::ffff:10.0.0.5`), and process paths (case, `\Device\HarddiskVolume3\`
  vs drive letters).
- Keep a `source`/`log_name` field so every event can be traced back to its original record.

## Tooling
Plaso (normalises to UTC internally), Timesketch for collaborative timelines, Logstash/Elastic
ingest pipelines, Splunk props/transforms (`TZ` per sourcetype), Python/pandas with
`pd.to_datetime(..., utc=True)`, DuckDB for ad hoc merges.

## Self-check
Every source in the timeline has a documented native zone, conversion method and measured skew,
and two independent events confirm alignment.
