---
id: computing-software.digital-forensics-incident-response.incident-response-process.intrusion-analysis-with-diamond-model-and-kill-chain
name: intrusion-analysis-with-diamond-model-and-kill-chain
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [diamond-model, kill-chain, intrusion-analysis, threat-intelligence, activity-threads, dfir]
level: advanced
status: draft
description: "Analyse intrusions with the Diamond Model and Lockheed Martin Kill Chain: events, pivots, activity threads, grouping campaigns and finding courses of action."
sources: ["https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf", "https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intrusion analysis with the Diamond Model and Kill Chain

**Goal:** structure intrusion evidence so analysts can pivot systematically, group related
activity, and find where defences can break the chain.

## Diamond Model (Caltagirone, Pendergast, Betz 2013)
Each **event** has four vertices: **adversary**, **capability** (malware, exploit),
**infrastructure** (domains, IPs, accounts), **victim** (person, host, asset), plus
meta-features: timestamp, phase, result, direction, methodology, resources.

### Analytic pivoting
From any vertex, pivot to the others:
- Infrastructure -> capability: what malware talks to this domain (sandbox, VT relations)?
- Capability -> infrastructure: other C2 in the same sample's config.
- Infrastructure -> infrastructure: passive DNS, WHOIS, TLS certificate reuse, JARM.
- Victim -> capability: what else ran on this host?
Record each pivot with source and confidence.

### Activity threads and groups
Chain events by phase into **activity threads** per victim; cluster threads sharing
capability/infrastructure/methodology into **activity groups** (what intel teams call
clusters, e.g. UNC groups) without forcing attribution to a named actor.

## Kill Chain (Hutchins, Cloppert, Amin 2011)
Reconnaissance, weaponisation, delivery, exploitation, installation, C2, actions on
objectives. Use it for **courses of action matrix**: for each phase, detect / deny /
disrupt / degrade / deceive / destroy. Indicators from later phases often reveal earlier
ones (C2 domain leads to delivery emails).
For technique-level detail map each event to MITRE ATT&CK; the models complement each other.

## Gotchas
- Shared infrastructure (CDNs, cloud IPs, compromised legitimate sites) produces false
  pivots; weight infrastructure by exclusivity.
- Attribution to named actors needs much more evidence than overlap of one indicator.

## Verify
Every diamond has sourced vertices, and the courses-of-action matrix has at least one
detection or mitigation per observed phase.
