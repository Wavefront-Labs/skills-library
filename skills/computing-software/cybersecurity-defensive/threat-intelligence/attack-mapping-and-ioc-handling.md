---
id: computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling
name: attack-mapping-and-ioc-handling
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [threat-intelligence, cti, mitre-attack, attack-navigator, ttps, detection-coverage, iocs, indicators-of-compromise, pyramid-of-pain, ioc-ageing, ioc-expiry, stix, taxii, misp, opencti, tlp, traffic-light-protocol, threat-intel-platform, sigma, yara, false-positives, sharing-communities]
level: practitioner
status: draft
description: "Map threat reports and detections to MITRE ATT&CK, prioritise TTPs over brittle IOCs, and ingest, age, share and retire indicators via STIX/TAXII and MISP under TLP."
sources: ["MITRE ATT&CK - Enterprise matrix and ATT&CK Navigator", "David Bianco - The Pyramid of Pain", "OASIS STIX 2.1 and TAXII 2.1 specifications", "FIRST Traffic Light Protocol (TLP) 2.0", "MISP Project documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ATT&CK mapping and IOC handling — use intel that changes what you detect

**Goal:** convert threat reports into detections and hunts mapped to ATT&CK, and run
an indicator pipeline that keeps IOCs useful (scored, aged, deconflicted) rather than
a growing blocklist of stale IPs.

## 1. Map reports to ATT&CK
1. Read the report and extract *behaviours*, one sentence each: "Used `rundll32` to
   load a DLL from `%AppData%`".
2. Map each to the most specific technique/sub-technique (e.g. T1218.011 Rundll32).
   Map what the evidence shows, not what the report's tags claim; note confidence.
3. Record procedure details (command lines, parent processes) — detections are
   built on procedures, not technique names.
4. Layer them in ATT&CK Navigator: one layer per priority threat group/report, one for
   your detection coverage. Overlay to see gaps (techniques used by relevant actors,
   no detection). Coverage is per *procedure*, so a green cell is not "solved".
Prioritise techniques that are used by actors targeting your sector *and* that you
have telemetry for; turn each into a Sigma rule or a hunt.

## 2. Pyramid of pain: weight your effort
From cheap-to-change up: hashes → IP addresses → domains → network/host artefacts →
tools → TTPs. Hash and IP blocks expire fast (attacker changes them trivially); detections
on artefacts and behaviours (named-pipe patterns, unusual parent-child processes,
tool command-line patterns) force real cost. Use IOCs for quick scoping and
retro-hunting; invest analyst time in TTP detections.

## 3. IOC ingest pipeline
- **Sources:** ISAC/ISAO feeds, national CERT, vendor reports, your own incidents
  (highest value). Store in a TIP: MISP or OpenCTI (open source) or a commercial platform.
- **Normalise:** STIX 2.1 objects (indicator, malware, threat-actor, relationships)
  delivered via TAXII 2.1 collections; MISP events with attributes, tags and galaxies.
- **Enrich and score:** source reliability, confidence, first/last seen, sightings.
- **Deconflict:** suppress against allowlists — top domains lists, your own IP space,
  CDN/cloud ranges, MISP warninglists (e.g. public DNS resolvers, RFC1918). Shared
  hosting IPs and CDN domains cause mass false positives if blocked.
- **Distribute** by type: domains/URLs to proxy and DNS RPZ, hashes to EDR, IPs to
  firewall/SIEM watchlists, all to SIEM for retro-search.

## 4. Ageing and expiry
Set default lifetimes per type and decay scores over time (MISP has decaying models).
Example starting points to tune: IPs 30–90 days, domains 90–180 days, URLs 30–90
days, file hashes long-lived (a hash never changes meaning) but low value. Re-extend
on fresh sightings. Expired IOCs leave active blocking but stay searchable for retro-hunts.

## 5. Sharing and TLP 2.0
- **TLP:RED** — named recipients only. **TLP:AMBER** — recipient's organisation and its
  clients on a need-to-know basis; **TLP:AMBER+STRICT** — organisation only.
  **TLP:GREEN** — the community, not public. **TLP:CLEAR** — public.
- Honour the marking of what you receive, including in tickets and SIEM notes.
- Share back: sightings and your own incident indicators (sanitised — no internal
  hostnames, usernames or customer data) strengthen the community feed.

## Gotchas
- Blocking an IOC with no expiry eventually blocks a legitimate service reusing the IP.
- Feeds overlap; the same IOC from five feeds isn't five times more credible if they all copy one source.
- ATT&CK versions update (techniques get deprecated or re-numbered) — pin the version in your coverage layer and review on releases.
- A retro-hunt hit on a 6-month-old IP is often a different, benign tenant; check timing against the report's activity window.
- Defanged IOCs (`hxxp`, `[.]`) pasted into tooling unconverted match nothing.

## Verify
- [ ] Priority threat reports have ATT&CK layers with procedure-level notes.
- [ ] A coverage layer shows detections per technique, with gaps feeding the detection backlog.
- [ ] IOCs are deduplicated, allowlist-filtered and scored before distribution.
- [ ] Every IOC type has a default expiry and expired ones leave blocklists automatically.
- [ ] TLP markings are preserved through the TIP, SIEM and tickets.
- [ ] Internal incident indicators are shared back after sanitisation.

Related: computing-software.cybersecurity-defensive.splunk.spl-detection-searches,
computing-software.cybersecurity-defensive.security-operations.alert-triage
