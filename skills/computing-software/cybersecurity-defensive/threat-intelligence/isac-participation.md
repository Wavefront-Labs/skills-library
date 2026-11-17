---
id: computing-software.cybersecurity-defensive.threat-intelligence.isac-participation
name: isac-participation
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [information-sharing, isac, isao, sharing-communities, tlp, misp-sharing, threat-sharing-governance]
level: practitioner
status: draft
description: "Join and get value from an ISAC or ISAO: select the community, set up legal and TLP governance, consume and contribute intel via portals and MISP, and measure the benefit."
sources: ["National Council of ISACs - member ISAC directory and guidance", "CISA - Information Sharing and Analysis Organizations (ISAO Standards Organization)", "FIRST Traffic Light Protocol 2.0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ISAC participation

**Goal:** a membership that delivers timely, relevant intel and peer contacts, with you contributing back safely.

## Choose the community
Sector ISACs (FS-ISAC, Health-ISAC, E-ISAC, MS-ISAC/CIS for US state and local government, Auto-ISAC, REN-ISAC for education, Retail & Hospitality ISAC), national schemes (UK NCSC CiSP successor services, EU sectoral ISACs), regional ISAOs, and trusted closed peer groups. Evaluate: membership cost tiers, member overlap with your threat profile, sharing platforms, 24x7 alerting, working groups.

## Governance before sharing
- Legal review of the membership agreement (confidentiality, liability, antitrust). In the US, the Cybersecurity Information Sharing Act of 2015 provides liability protections for sharing cyber threat indicators per its procedures.
- Internal sharing policy: who may share, what (indicators, TTPs, incident summaries), anonymisation, approval path (CTI lead + legal for incident details), TLP handling.
- Remove personal data and customer identifiers from shared material.

## Consume
- Integrate feeds (MISP/TAXII) into your TIP with source tagging and reliability ratings.
- Route alerts (vulnerability exploitation, campaigns against the sector) to SOC/vuln management with your relevance assessment.
- Attend working groups and exercises; build personal contacts - the most valuable sharing is often analyst-to-analyst during incidents.

## Contribute
Share sightings of campaigns, phishing samples (sanitised), IOCs with context, detection rules. Even "we saw this too" sightings increase confidence for others. Respect TLP (TLP:AMBER+STRICT stays within your organisation; TLP:AMBER may go to clients on need-to-know).

## Measure value
Track: alerts received that were relevant, detections/blocks sourced from ISAC intel, incidents where peer contact helped, contributions made. Review at renewal.

## Verify
- [ ] Sharing policy approved by legal and published to the CTI team.
- [ ] ISAC feed ingested with source tag; monthly metrics recorded.
