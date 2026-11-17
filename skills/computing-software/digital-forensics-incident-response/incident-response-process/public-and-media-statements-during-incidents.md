---
id: computing-software.digital-forensics-incident-response.incident-response-process.public-and-media-statements-during-incidents
name: public-and-media-statements-during-incidents
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [media-statement, public-relations-incident, crisis-communications, incident-communications, dfir]
level: practitioner
status: draft
description: "Coordinate public, customer and media statements during a cyber incident with legal and PR: holding statements, approval, consistency and what never to say."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.ncsc.gov.uk/collection/incident-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Public and media statements during incidents

**Goal:** say something accurate early, never contradict it later, and never create legal
exposure or tip off the attacker.

## Prepare in advance
- Pre-approved **holding statements** for: service outage of unknown cause, confirmed cyber
  incident under investigation, ransomware, data exposure.
- Approval chain: comms lead drafts, technical lead fact-checks, legal approves, exec signs.
- Spokesperson named and media-trained; everyone else refers enquiries to the press office.

## Holding statement example
"We are investigating a cybersecurity incident affecting some of our systems. We took
immediate steps to contain it, engaged external specialists and notified the relevant
authorities. Our investigation is ongoing and we will provide updates at <URL>."

## Rules
- Every public fact must be **confirmed by forensics**. "No customer data was accessed" in
  week one is the classic mistake; say "we have not found evidence that..." only if true.
- Consistency across channels: website, customer emails, support scripts, investor
  disclosure (SEC 8-K) and regulator notifications must not contradict each other.
- Do not name the threat actor or confirm ransom details; it complicates negotiation and law
  enforcement work.
- Do not publish IOCs or technical detail that reveals what you know while the attacker may
  still be present.
- Watch social media and leak sites; the attacker may publish first. Have a response ready
  for "the group claims to have X TB of data".
- Employees: brief them on what to say to customers and remind them not to post.

## After
Archive every published statement with timestamp; regulators and litigants will compare them
with your later findings.

## Verify
Tabletop inject: a journalist calls the help desk at hour 3. Was the call routed correctly and
did anyone deviate from the holding line?
