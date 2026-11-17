---
id: computing-software.cybersecurity-defensive.threat-intelligence.cyber-kill-chain-analysis
name: cyber-kill-chain-analysis
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [adversary-profiling, cyber-kill-chain, intrusion-kill-chain, courses-of-action, defence-in-depth, campaign-analysis]
level: practitioner
status: draft
description: "Apply the Lockheed Martin Cyber Kill Chain to intrusions and campaigns: map events to phases, build a courses-of-action matrix and identify where defences broke the chain."
sources: ["Hutchins, Cloppert, Amin - Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains (Lockheed Martin, 2011)", "SANS FOR578 Cyber Threat Intelligence", "MITRE ATT&CK - relationship to kill chain models"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cyber Kill Chain analysis

**Goal:** analyse an intrusion or campaign by phase to find where you detected or could have disrupted it, and plan controls for each phase.

## Phases
1. Reconnaissance - target research, scanning, harvesting emails.
2. Weaponization - coupling exploit with payload (malicious document, loader) - mostly invisible to defenders, inferred from artefacts.
3. Delivery - email, web, USB, exposed service.
4. Exploitation - code executes (vuln exploit, user enables macros).
5. Installation - persistence (implant, scheduled task, web shell).
6. Command and Control - channel to operator.
7. Actions on Objectives - data theft, encryption, destruction, lateral movement toward the goal.

## Courses of action matrix
Rows = phases, columns = Detect, Deny, Disrupt, Degrade, Deceive, Destroy (original paper). Fill with your actual controls, e.g.:
- Delivery: Detect - email gateway sandbox; Deny - attachment type blocking.
- Installation: Detect - EDR persistence alerts; Deny - application control.
- C2: Detect - DNS/proxy analytics; Deny - egress filtering; Degrade - throttling; Deceive - sinkholing.

## Campaign analysis
Compare multiple intrusions by the same actor phase by phase; indicators that recur in early phases (delivery infrastructure, weaponization artefacts like builder metadata) let you stop later attempts earlier. An intrusion stopped at Delivery still yields intel for the campaign.

## Limitations
Linear and perimeter-centric; insider, cloud identity and supply-chain attacks fit awkwardly. Use with ATT&CK for technique detail and the Diamond Model for pivoting; the Unified Kill Chain extends phases for post-compromise activity.

## Verify
- [ ] IR reports include phase mapping with the phase where detection occurred.
- [ ] COA matrix has at least one Detect and one Deny control for Delivery through C2, or a recorded gap.
