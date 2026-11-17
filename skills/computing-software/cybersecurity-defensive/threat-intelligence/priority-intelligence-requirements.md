---
id: computing-software.cybersecurity-defensive.threat-intelligence.priority-intelligence-requirements
name: priority-intelligence-requirements
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [intelligence-lifecycle, priority-intelligence-requirements, pir, intelligence-requirements, stakeholder-analysis, direction-phase]
level: advanced
status: draft
description: "Define priority intelligence requirements with stakeholders: elicit decisions they face, write PIRs and EEIs, prioritise, map to collection and review them on a schedule."
sources: ["SANS FOR578 Cyber Threat Intelligence - Requirements", "CREST - What is Cyber Threat Intelligence and how is it used", "US Joint Publication 2-0 Joint Intelligence (intelligence requirements)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Priority intelligence requirements

**Goal:** a short, owned list of questions the CTI team answers, tied to decisions, which drives collection and reporting.

## Elicit
Interview stakeholders (CISO, SOC lead, IR, vuln management, fraud, executives, product security). Ask: what decisions do you make, what would change them, what happened last year that surprised you, what assets would hurt most?

## Write
- **PIR** (decision-level question): "Which threat actors are likely to target our payment platform in the next 12 months, and how?"
- **Specific intelligence requirements / EEIs** (answerable pieces): "Which ransomware affiliates are exploiting the edge VPN products we run?", "Are our customer credentials sold on access markets?"
- Each with: stakeholder, decision supported, priority, time horizon, product format (alert, weekly brief, assessment), review date.

## Prioritise
Rank by business impact and likelihood; cap active PIRs (around 5-10) so the team can actually answer them. Separate standing requirements (ongoing) from ad hoc requests (RFIs) with a request form.

## Map to collection and products
For each EEI list sources (internal telemetry, ISAC, vendor intel, OSINT, dark web monitoring) and the product that answers it. Gaps in collection become budget arguments.

## Review
Quarterly with stakeholders: is each PIR still relevant, were products useful, which decisions did they inform? Retire or rewrite.

## Gotchas
- "Tell us about all threats" is not a requirement.
- Requirements written by the CTI team alone reflect analyst interests, not stakeholder decisions.
- No feedback loop means the list fossilises.

## Verify
- [ ] Each PIR has a named stakeholder and a product delivered in the last quarter.
- [ ] RFIs are logged and mapped to PIRs or new requirements.
