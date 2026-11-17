---
id: computing-software.cybersecurity-defensive.threat-intelligence.mitre-engage-adversary-engagement
name: mitre-engage-adversary-engagement
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [mitre-engage, attack-mapping, deception, adversary-engagement, honeytokens, cyber-denial]
level: advanced
status: draft
description: "Plan defensive adversary engagement with MITRE Engage: goals, approaches and activities (deception, denial), engagement planning cycle and safety considerations."
sources: ["https://engage.mitre.org/", "https://engage.mitre.org/matrix/", "https://d3fend.mitre.org/tactic/d3f:Deceive/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MITRE Engage

Engage is MITRE's framework for adversary engagement: using denial and deception to expose,
affect and elicit information about adversaries. It is the defensive deception counterpart to ATT&CK.

## Matrix
- **Strategic goals**: Prepare, Understand (plan and learn).
- **Engagement goals**: Expose (detect adversaries), Affect (disrupt/deny their operations),
  Elicit (learn about them).
- **Approaches** per goal (e.g. Expose: Collect, Detect; Affect: Prevent, Direct, Disrupt; Elicit:
  Reassure, Motivate) and **activities** (e.g. Lures, Decoy Artifacts and Systems, Network Manipulation,
  Software Manipulation, Pocket Litter, Introduced Vulnerabilities, Burn-In).
- Each activity links to ATT&CK techniques it can exploit (adversary vulnerabilities): e.g. adversaries
  enumerating credentials (T1552) can be engaged with decoy credentials.

## Planning cycle (10 steps in the Engage handbook, condensed)
1. Assess knowledge of the adversary and your environment.
2. Determine operational objective (e.g. early detection of lateral movement).
3. Determine how you want the adversary to react and what you want them to perceive.
4. Choose activities (decoy accounts, honey files, canary tokens, decoy hosts).
5. Define rules of engagement, gating criteria, and safety (no harm to production, legal review).
6. Implement, monitor, analyse, refine; capture lessons.

## Practical starting points
- Honeytokens: fake AWS keys (canarytokens), decoy admin accounts with alerting on any logon
  (4624/4625 for the account), decoy files in shares, DNS canaries.
- Decoy services in each network segment (OpenCanary, commercial deception platforms).
Map each to Engage activities and ATT&CK techniques for coverage reporting.

## Gotchas
- Deception assets must be indistinguishable yet harmless; review with legal and operations.
- Alerts from decoys are high fidelity; route as P1/P2, not to a dashboard.

## Verify
Engagement plan document with objectives, activities mapped to Engage IDs, monitoring and RoE;
purple-team test triggers each decoy alert.
