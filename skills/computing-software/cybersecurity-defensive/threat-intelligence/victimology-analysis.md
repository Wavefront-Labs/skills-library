---
id: computing-software.cybersecurity-defensive.threat-intelligence.victimology-analysis
name: victimology-analysis
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [victimology, adversary-profiling, threat-actor-profiling, diamond-model, threat-relevance, targeting-analysis]
level: practitioner
status: draft
description: "Analyse victimology for threat actors and campaigns: sector, geography, organisation size, technology and role targeting, and turning it into relevance assessments."
sources: ["https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf", "https://www.sans.org/white-papers/", "https://attack.mitre.org/groups/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Victimology

Victimology is the study of who an adversary targets and why; in the Diamond Model it is the
**victim** vertex (persona and assets).

## Dimensions
- **Sector and sub-sector** (e.g. healthcare -> hospitals vs medical device makers).
- **Geography** and language.
- **Organisation size/revenue** (ransomware affiliates and IABs often target specific revenue bands).
- **Technology** (exploited products: specific VPNs, file transfer appliances, ERP).
- **Roles targeted** (finance staff for BEC, developers for supply chain, executives, IT admins).
- **Data or capability sought** (IP, payment data, access to customers/MSPs).
- **Timing** (around geopolitical events, holidays, financial periods).

## Sources
Incident reports (yours and shared via ISAC), vendor reports, leak site postings (victim lists),
government advisories, court documents.

## Method
1. Build a victim dataset per actor/campaign with the dimensions above.
2. Identify patterns and changes over time (expansion into new sectors, new exploited technology).
3. Compare to your organisation's profile: overlap on sector, geography, technology stack, size.
4. Output relevance rating with confidence for each tracked actor (e.g. "High: targets EU
   manufacturing using Citrix NetScaler, which we run").

## Use
- Prioritise detection/hunting and vulnerability remediation for actors with high victim overlap.
- Inform tabletop scenarios and PIRs.

## Gotchas
- Visibility bias: reported victims skew toward sectors with disclosure obligations or vendor customer bases.
- Opportunistic actors' victimology is "whoever is vulnerable" - technology exposure matters more than sector.

## Verify
Actor relevance ratings cite victimology evidence and are reviewed when new reporting shifts patterns.
