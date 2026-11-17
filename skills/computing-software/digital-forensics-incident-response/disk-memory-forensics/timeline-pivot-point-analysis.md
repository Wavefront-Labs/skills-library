---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.timeline-pivot-point-analysis
name: timeline-pivot-point-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [pivot-point-analysis, super-timeline, timeline-explorer, plaso, dfir]
level: advanced
status: draft
description: "Work a super timeline efficiently: choose pivot points, read temporal proximity, filter noise, tag findings and iterate across hosts without drowning in events."
sources: ["https://plaso.readthedocs.io/", "https://www.sans.org/cyber-security-courses/advanced-incident-response-threat-hunting-training/", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timeline pivot-point analysis

**Goal:** a super timeline holds millions of rows. Analysts succeed by starting from a known
event and reading outward, not by scrolling from the top (FOR508 timeline analysis method).

## 1. Pick pivot points
- Alert time and artefact (EDR detection, AV hit, suspicious login).
- A known-bad file (path, name, hash) - its MFT birth time, prefetch first run.
- An account and logon (4624 with logon ID).
- A network event (first C2 connection from proxy logs).
Write each pivot with UTC time and source in the case notes.

## 2. Read temporal proximity
- Filter the timeline to +/- 5-15 minutes around the pivot; read every event in order.
- Typical clusters: download (browser history, Zone.Identifier ADS, $MFT create) -> execution
  (prefetch, Amcache, 4688) -> persistence (registry key last-write, service 7045, task XML) ->
  credential access/lateral movement.
- Each new suspicious artefact becomes a new pivot (path, user, time).

## 3. Reduce noise
- Exclude known-noise sources (Windows Update, AV scans, defrag/indexer access times) by
  parser/source and path filters; keep a saved filter set.
- Collapse repeated rows (same path, same second) and focus on MACB birth (`B`) events for new files.
- In Timeline Explorer: column filters, `Ctrl+F` find, tag rows (`Tag` column), colour by `SourceDescription`.

## 4. Record findings
- Tag every relevant row; export tagged rows to the master incident timeline with a one-line interpretation.
- Note gaps (no events for hours) and whether that means "off", "idle" or "logs missing".

## 5. Iterate across hosts
- Use account names, hashes, IPs and times from host A as pivots on host B's timeline, and on enterprise logs.

## Gotchas
- Time zone mix-ups: normalise all sources to UTC at creation (`psort --output_time_zone UTC`).
- Access times are unreliable (disabled updates, AV scanning); weight birth and modification times.
- Tool clock: timeline only as good as the host clock; check clock skew against network logs.

## Verify
Each key event in the incident narrative is backed by tagged timeline rows from at least two sources.
