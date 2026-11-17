---
id: computing-software.cybersecurity-defensive.security-operations.ir-retainer-and-third-party-dfir
name: ir-retainer-and-third-party-dfir
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [ir-retainer, dfir, incident-response, third-party-forensics, legal-privilege, cyber-insurance]
level: advanced
status: draft
description: "Set up and use an incident response retainer with a third-party DFIR firm: scope, SLAs, pre-engagement onboarding, privilege, data handling and how to engage under pressure."
sources: ["https://www.ncsc.gov.uk/information/cyber-incident-response-scheme", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/sites/default/files/2023-01/ransomware-guide-september-2020.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# IR retainer and third-party DFIR engagement

## Choosing
- Check your cyber insurer's panel first: insurers often require panel firms for coverage.
- Capabilities: ransomware, BEC, cloud (M365/AWS/Azure), OT if relevant, negotiation, recovery;
  jurisdictions and languages; certifications (CREST CIR, NCSC CIR in the UK).
- Commercials: pre-paid hours (usable for proactive work if unused), response SLA (remote within
  hours, on-site within N hours), rates, surge capacity.

## Pre-engagement onboarding (do it in peacetime)
- MSA and SOW signed, ideally contracted by outside counsel for privilege.
- Exchange contacts and a 24/7 hotline; agree out-of-band communications (if email/Teams are
  compromised, use Signal or phone bridges).
- Technical onboarding: their EDR/forensic tooling approved for emergency deployment, network
  diagrams, asset lists, log source inventory, admin contacts; test agent deployment once.
- Data handling: where evidence is stored, retention, deletion on closure, regulated data rules.

## Engaging
1. Call counsel and insurer (notification deadlines can be 24-72 h), then the DFIR hotline.
2. Kick-off: scope, objectives (contain, scope, root cause, attestation for regulators), daily
   cadence, roles (who directs the firm: counsel or CISO).
3. Grant access through a controlled path; log their actions.
4. Get written daily updates; insist on preliminary findings before final report.

## Gotchas
- Reports drafted by the firm under counsel may be privileged; avoid sharing drafts widely.
- Firms work fast but need your environment knowledge; assign a technical liaison full time.
- Retainer hours expire; use leftovers for tabletop, compromise assessment or IR plan review.

## Verify
Annual test: call the hotline in a tabletop, confirm SLA response, and confirm onboarding info is current.
