---
id: computing-software.cybersecurity-defensive.threat-intelligence.diamond-model-analysis
name: diamond-model-analysis
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [adversary-profiling, diamond-model, intrusion-analysis, activity-threads, pivoting, adversary-capability-infrastructure-victim]
level: advanced
status: draft
description: "Use the Diamond Model of Intrusion Analysis to structure events by adversary, capability, infrastructure and victim, pivot between vertices, and build activity threads and groups."
sources: ["Caltagirone, Pendergast, Betz - The Diamond Model of Intrusion Analysis (2013)", "SANS FOR578 Cyber Threat Intelligence - Diamond Model", "ThreatConnect - Diamond Model analytic pivoting guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diamond Model analysis

**Goal:** organise intrusion data so analysts can pivot systematically and cluster related activity.

## Core features of an event
- **Adversary** - operator/customer (often unknown at first).
- **Capability** - malware, exploits, tools, techniques.
- **Infrastructure** - IPs, domains, email accounts, C2 servers (type 1 adversary-owned, type 2 compromised intermediaries).
- **Victim** - persona (organisation, person) and assets (host, account, email address).
Meta-features: timestamp, phase (kill chain), result, direction, methodology, resources. Socio-political (adversary-victim relationship/intent) and technology (capability-infrastructure link) axes.

## Pivoting
From any known vertex, ask what links to the next:
- Infrastructure -> capability: what malware talked to this C2 (sandbox/VT relations)?
- Infrastructure -> infrastructure: passive DNS, WHOIS registrant, TLS certificate, hosting patterns, JARM/JA4S.
- Capability -> infrastructure: config extraction from samples reveals more C2s.
- Victim -> capability: what else hit this victim (internal telemetry)?
Record each pivot with confidence; low-confidence links (shared hosting IP) should not drive conclusions.

## Activity threads and groups
- **Activity thread:** ordered diamonds for one intrusion across kill-chain phases, including hypothesised (unseen) events that should exist - gaps become hunting leads.
- **Activity group:** clustering threads with shared features (same capability + infrastructure patterns + victimology) into a named group (internal naming before mapping to vendor names).

## Output
Diamond per event in the TIP (MISP objects/OpenCTI relationships), thread diagram for IR reports, group profile for CTI.

## Gotchas
- Equating an activity group with a named nation-state actor without strong evidence.
- Ignoring the victim vertex; victimology often reveals intent.

## Verify
- [ ] Each event records all four vertices (unknowns marked) and the pivot source for each link.
- [ ] Activity group definitions list the features used for clustering.
