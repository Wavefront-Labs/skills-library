---
id: computing-software.cybersecurity-defensive.threat-intelligence.unified-kill-chain-analysis
name: unified-kill-chain-analysis
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [unified-kill-chain, adversary-profiling, kill-chain, attack-mapping, intrusion-analysis, mitre-attack]
level: practitioner
status: draft
description: "Analyse intrusions with the Unified Kill Chain: 18 phases across In, Through and Out, compared with Lockheed kill chain and ATT&CK, for mapping attacks and defences."
sources: ["https://www.unifiedkillchain.com/", "https://www.unifiedkillchain.com/assets/The-Unified-Kill-Chain.pdf", "https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Unified Kill Chain

Paul Pols' Unified Kill Chain (UKC) combines the Lockheed Martin Cyber Kill Chain and MITRE ATT&CK into
18 phases, addressing the linear kill chain's focus on the perimeter and malware.

## Phases
- **In** (initial foothold): Reconnaissance, Resource Development, Delivery, Social Engineering,
  Exploitation, Persistence, Defense Evasion, Command & Control.
- **Through** (network propagation): Pivoting, Discovery, Privilege Escalation, Execution,
  Credential Access, Lateral Movement.
- **Out** (action on objectives): Collection, Exfiltration, Impact, Objectives.
Phases can repeat and be skipped; attacks are cycles, not a straight line.

## Using it
- **Incident analysis**: lay out the attacker's sequence of phases with ATT&CK techniques under each;
  shows where they looped (e.g. multiple Through cycles across domains).
- **Defence mapping**: map controls and detections to phases; aim for layered coverage in each of In,
  Through, Out so that a miss at the perimeter is caught later.
- **Communication**: UKC phases are coarser than ATT&CK tactics and easier for non-specialists but more
  realistic than the 7-step kill chain.
- **Red/purple team scoping**: define scenarios starting at Through (assumed breach) to test internal
  detection.

## Compared
- Cyber Kill Chain: 7 phases, perimeter/malware-centric, linear.
- ATT&CK: 14 enterprise tactics, technique-level detail, no ordering.
- UKC: ordered phases plus ATT&CK detail, includes social engineering and objectives explicitly.

## Verify
Post-incident report includes a UKC phase diagram with techniques and the controls that detected/failed
at each phase.
