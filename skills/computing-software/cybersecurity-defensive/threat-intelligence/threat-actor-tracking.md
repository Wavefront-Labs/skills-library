---
id: computing-software.cybersecurity-defensive.threat-intelligence.threat-actor-tracking
name: threat-actor-tracking
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [adversary-profiling, threat-actor-tracking, activity-clustering, actor-naming, threat-actor-profiles, attribution-confidence]
level: advanced
status: draft
description: "Track threat actors over time: maintain internal activity clusters and profiles, map vendor naming overlaps carefully, update TTP and infrastructure patterns and record attribution confidence."
sources: ["MITRE ATT&CK Groups (naming and associated groups)", "Microsoft - How Microsoft names threat actors", "Mandiant - UNC and FIN/APT naming and graduation process"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat actor tracking and clustering

**Goal:** consistent, evidence-based profiles of the actors that matter to you, updated as activity occurs.

## Internal clusters first
Start with your own designators for observed activity (e.g. `CLUSTER-2026-07`), defined by overlapping indicators: capability (custom malware family, builder artefacts), infrastructure patterns (registrar, naming scheme, hosting, certificate reuse, JA4S), victimology, and TTP sequences. Merge clusters only with strong overlaps; document merge decisions (Mandiant's UNC-to-named-group graduation is a model).

## Mapping to public names
Vendors name the same or overlapping activity differently (APT29 / Midnight Blizzard / NOBELIUM / Cozy Bear). ATT&CK Groups lists associated names; overlaps are often partial. Record the mapping as "overlaps with" plus confidence, not as identity.

## Profile contents
- Names/aliases and the sources linking them.
- Motivation and likely sponsor (with confidence), targeted sectors/regions, relevance to us.
- TTPs as an ATT&CK layer with procedure examples and dates.
- Tooling and malware families; infrastructure patterns; known exploited CVEs.
- Timeline of activity (public reporting + internal sightings).
- Detection and hunting content mapped to the actor; gaps.
- Last reviewed date and analyst.

## Maintenance
- New reporting triggers an update; stale profiles (> 6 months) flagged.
- Track TTP changes (e.g. shift from phishing to edge device exploitation) since that changes defensive priorities.
- Store as STIX `intrusion-set`/`threat-actor` objects in the TIP with relationships.

## Gotchas
- Attribution by tool alone - many tools are shared or leaked (Cobalt Strike, Sliver, leaked ransomware builders).
- False flags and contractors serving multiple sponsors.
- Over-investing in attribution when the defensive actions are identical.

## Verify
- [ ] Priority actors have profiles reviewed in the last 6 months with ATT&CK layers.
- [ ] Cluster definitions and merges are documented with evidence.
