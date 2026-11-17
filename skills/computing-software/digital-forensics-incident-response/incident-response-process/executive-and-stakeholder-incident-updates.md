---
id: computing-software.digital-forensics-incident-response.incident-response-process.executive-and-stakeholder-incident-updates
name: executive-and-stakeholder-incident-updates
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [stakeholder-updates, executive-briefing, incident-communications, sitrep, dfir]
level: practitioner
status: draft
description: "Write executive and stakeholder status updates during an incident: cadence, a fixed sitrep template, facts versus assessments, and decisions needed."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.ncsc.gov.uk/collection/incident-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Executive and stakeholder incident updates

**Goal:** leaders get a predictable, accurate picture and know exactly which decisions they
must make, without derailing the technical team.

## Cadence
- SEV1: written sitrep every 4 h (or at each bridge), exec call daily.
- SEV2: twice daily, then daily.
- Announce the next update time in every update and keep it, even if "no change".

## Sitrep template (keep it to one screen)
```
INCIDENT <codename> | SEV<n> | Update #<k> | <UTC time> | Next update <time>
BOTTOM LINE: one sentence on where we are.
WHAT WE KNOW (confirmed):    - ...
WHAT WE ASSESS (confidence):  - likely ... (moderate)
WHAT WE DON'T KNOW YET:      - ...
IMPACT: business services, data, customers, regulatory clock (e.g. GDPR 72h started <time>)
ACTIONS SINCE LAST UPDATE:   - ...
NEXT ACTIONS / OWNERS:       - ...
DECISIONS NEEDED (by when):   - Approve shutdown of X by 14:00 UTC (owner: COO)
```

## Writing rules
- Separate fact, assessment and unknown. Executives forgive "we don't know yet"; they do not
  forgive a confident statement retracted next day.
- Use confidence words consistently (low/moderate/high) and say what would change them.
- Business language: "payroll is down for 3,000 staff", not "DC02 is isolated".
- No speculation about attribution or the attacker's identity.
- Updates may be discoverable; counsel reviews wording, mark "Privileged and confidential,
  prepared at the direction of counsel" only when that is actually true.

## Stakeholder map
Board / audit committee, executive team, affected business owners, customer-facing teams
(support scripts), employees (what to do / not do), third parties under contract.

## Verify
Ask a non-technical exec to read a sample update and state the decision they must make; if
they cannot in 30 seconds, rewrite.
