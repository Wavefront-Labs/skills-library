---
id: computing-software.cybersecurity-defensive.security-architecture.crisis-management
name: crisis-management
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [crisis-management, crisis-management-team, incident-command, executive-decision-making, crisis-communications, cyber-crisis, tabletop-exercise]
level: advanced
status: draft
description: "Stand up a crisis management team for a major cyber incident: membership, activation, decision log, cadence, communications, regulatory clocks and exercising."
sources: ["https://www.iso.org/standard/50003.html", "https://www.ncsc.gov.uk/collection/incident-management/cyber-incident-response-processes", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crisis management team

The technical incident team fixes systems; the crisis management team (CMT) makes business decisions:
pay or not, notify whom, shut down what, what to say publicly.

## Membership
Exec chair (CEO/COO delegate), CISO/incident lead (briefs, does not run the technical response here),
Legal/external counsel, Communications/PR, HR, Finance, Operations/business owners, Risk/insurance.
Named deputies for each.

## Activation
Pre-defined triggers: business-critical service outage beyond MTPD, suspected data breach of regulated
data, extortion demand, media interest, safety impact. Any CMT member can call it.

## Running it
- Cadence: fixed situation briefings (e.g. every 4 hours) with a standard format: facts, unknowns, impact, options, decisions needed.
- **Decision log:** time, decision, options considered, rationale, owner. Critical for regulators, insurers and litigation.
- Separate rooms/channels from the technical team; liaison carries information both ways.
- Out-of-band communications (assume email/Teams compromised): pre-provisioned Signal group or alternative tenant, printed contact sheet.

## Clocks to track
GDPR 72 h to the supervisory authority, NIS2 24 h early warning / 72 h notification, SEC 8-K 4 business
days after materiality, contractual notice periods, cyber insurer notification terms.

## Communications
Holding statements pre-drafted for staff, customers, media. One spokesperson. Legal review, but speed matters.

## Exercise
Annual executive tabletop with injects (ransom note, journalist call, regulator query, backups also encrypted).

## Gotchas
- Executives dragged into technical detail; the CISO filters.
- Engaging counsel early to preserve privilege on forensic reports.
- Fatigue: rotate roles on multi-day incidents.

## Verify
- [ ] CMT roster with deputies and out-of-band contacts current.
- [ ] Decision log template and holding statements ready.
- [ ] Exercise in last 12 months.
