---
id: computing-software.cybersecurity-defensive.threat-intelligence.national-cert-coordination
name: national-cert-coordination
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [cert-coordination, information-sharing, national-csirt, nis2, incident-reporting, cisa, ncsc]
level: practitioner
status: draft
description: "Coordinate with national CERTs/CSIRTs during incidents and campaigns: when to engage, mandatory reporting channels (NIS2, CIRCIA), what they offer and how to share effectively."
sources: ["https://www.enisa.europa.eu/topics/incident-response/csirts-in-europe", "https://www.first.org/members/teams", "https://www.cisa.gov/report"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# National CERT coordination

## Who they are
National CSIRTs/CERTs: CISA (US), NCSC (UK), CERT-EU (EU institutions), national CSIRTs under NIS2
(e.g. CERT-FR/ANSSI, BSI CERT-Bund, NCSC-NL), JPCERT/CC, CERT-In (India, with 6-hour reporting rule).
Directory via FIRST members list and ENISA CSIRTs network.

## When to engage
- Mandatory reporting: NIS2 essential/important entities (early warning within 24 h, notification within
  72 h, final report within one month to the CSIRT or competent authority); sector rules; CERT-In
  directions; CIRCIA for US covered entities once in force.
- Voluntary: significant incidents, campaigns affecting others, vulnerabilities in widely used products,
  need for assistance (CISA and NCSC offer incident response support to some entities).

## What they provide
Victim notifications (they may contact you first about compromised systems observed in sinkhole
or scan data), advisories and IOCs, coordination across affected organisations, liaison with law
enforcement and international CERTs, vulnerability coordination.

## Sharing effectively
- Single point of contact in your IR plan with pre-established relationship (register on their portals).
- Provide concise facts: timeline, affected systems, IOCs (STIX/MISP export), TLP marking, what help you need.
- Agree how they may use and share your information (anonymisation).

## Receiving notifications
Treat CERT victim notifications as high priority: verify through official channels (attackers
impersonate CERTs), then investigate the reported IP/system.

## Gotchas
- Different authorities per sector/country; map obligations in advance for multinational operations.
- Reporting deadlines run from awareness, not confirmation.

## Verify
IR plan lists CERT contacts and reporting obligations per jurisdiction; exercises include a CERT
notification step with timing measured.
