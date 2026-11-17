---
id: computing-software.cybersecurity-defensive.threat-intelligence.intelligence-collection-plan
name: intelligence-collection-plan
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [intelligence-lifecycle, collection-plan, collection-management, source-evaluation, admiralty-code, collection-gaps]
level: advanced
status: draft
description: "Build and run a CTI collection plan: map requirements to sources, evaluate sources with reliability ratings, track coverage gaps and retire low-value feeds."
sources: ["SANS FOR578 Cyber Threat Intelligence - Collection", "NATO Admiralty Code / STANAG 2511 source reliability and information credibility", "FIRST CTI SIG curriculum - Collection"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Collection management

**Goal:** every intelligence requirement has sources assigned, sources are evaluated, and gaps are known.

## Collection plan matrix
Rows = EEIs (from PIRs). Columns: source, source type (internal telemetry, ISAC, commercial, OSINT, closed forums, partner, human), access method, cost, frequency, owner, reliability rating, last value delivered.

## Source types
- Internal: incident data, SIEM/EDR telemetry, phishing reports, honeypots, malware sandbox results - often the most relevant.
- Communities: ISACs, CERT/CSIRT notifications, trusted peer groups.
- Commercial: vendor intel portals and feeds.
- OSINT: vendor blogs, CISA/NCSC advisories, social media, code repos, paste sites, CT logs.
- Restricted: dark web/criminal forums (legal and OPSEC review needed; use a provider if you lack sanctioned capability).

## Evaluate
- Admiralty code: source reliability A (completely reliable) to F (cannot be judged); information credibility 1 (confirmed) to 6 (cannot be judged). Tag each item, e.g. B2.
- Periodically score each source on relevance to PIRs, timeliness, uniqueness (overlap with others), false positive rate, and actionability.

## Gap management
- EEIs with no or only low-reliability sources = collection gaps; propose sources (new feed, ISAC membership, internal logging change).
- Feeds that never contribute to products or detections over 2 quarters are candidates for cancellation.

## OPSEC and legal
Use attribution-managed infrastructure for researching adversary sites; follow legal guidance on accessing criminal marketplaces, purchasing data, and handling stolen data (often prohibited).

## Verify
- [ ] Collection matrix covers all active EEIs.
- [ ] Sources have current ratings and an owner.
- [ ] Gap list reviewed with CTI lead quarterly.
