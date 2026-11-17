---
id: computing-software.digital-forensics-incident-response.incident-response-process.tracking-iocs-and-affected-assets
name: tracking-iocs-and-affected-assets
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ioc-tracking, affected-asset-tracking, scoping, iocs, case-tracking, dfir]
level: practitioner
status: draft
description: "Track indicators and affected assets through an incident: IOC register, asset status states, sweep results, and keeping scope current until closure."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://docs.dfir-iris.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking IOCs and affected assets

**Goal:** at any moment the team can answer "which hosts and accounts are affected, what is
their state, and which indicators have we swept for?"

## IOC register
| Field | Notes |
|---|---|
| Value, type | sha256, domain, IP, URL, mutex, service name, registry path, user agent, account |
| First / last seen | Times from evidence, not when you added it |
| Source | Evidence ID or intel report |
| Confidence | High (seen on our hosts) / medium / low (third-party intel only) |
| Status | Swept? Blocked? Detection rule deployed? |
| Shareable (TLP) | For MISP/ISAC export at closure |

Prefer **behavioural and host indicators** (paths, service names, command-line patterns,
named pipes) over IPs/hashes, which attackers rotate (Pyramid of Pain).

## Asset register states
`suspected` -> `confirmed compromised` -> `contained` -> `eradicated` -> `recovered` ->
`monitoring`; plus `cleared` (investigated, not compromised). Each transition needs evidence
and a timestamp. Track accounts the same way (credentials exposed, reset, MFA re-enrolled).

## Sweeps
- Each new IOC gets swept across the estate (EDR search, Velociraptor hunt, SIEM query) and
  the sweep date and coverage (% hosts online) recorded.
- New hits feed back as newly suspected assets; re-sweep older IOCs after scope grows.

## Gotchas
- Hosts offline during the sweep are not "clean"; schedule a re-sweep when they return.
- Dedupe hosts by asset ID, not hostname (renames, re-imaging).
- Remove false-positive IOCs explicitly with a note rather than deleting them.

## Verify
Before declaring eradication, every confirmed host must be in `eradicated` or later, every
high-confidence IOC swept within the last 72 h with coverage above the agreed threshold.
