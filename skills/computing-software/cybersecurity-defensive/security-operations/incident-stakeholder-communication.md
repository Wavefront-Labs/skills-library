---
id: computing-software.cybersecurity-defensive.security-operations.incident-stakeholder-communication
name: incident-stakeholder-communication
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-reporting, stakeholder-communication, incident-communications, status-updates, out-of-band-communication, comms-cadence, crisis-communication]
level: practitioner
status: draft
description: "Run incident communications: stakeholder map, update cadence and templates, out-of-band channels and coordination with legal, PR and customers."
sources: ["NIST SP 800-61r3 (communication and information sharing)", "CSF 2.0 RS.CO-02/RS.CO-03 and RC.CO", "CISA Incident Response Playbook (coordination)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stakeholder communication during incidents

**Goal:** the right people get accurate, timely updates through channels the attacker cannot
read, and nobody makes conflicting statements.

## Stakeholder map (prepare before incidents)
| Audience | Needs | Owner | Channel |
|---|---|---|---|
| Incident team | Tasks, findings | Incident commander | Out-of-band chat + bridge |
| Executives | Impact, decisions, ETA | IC or CISO | Scheduled briefings |
| IT/ops | Actions required | IT lead | Bridge / tickets |
| Employees | What to do or not do | Comms + CISO | Approved internal message |
| Legal / privacy / DPO | Facts for notification decisions | Legal | Privileged channel |
| Customers / partners | Impact on them | Comms + account owners | Approved statements |
| Regulators / law enforcement | Mandated notifications | Legal | Formal |
| Insurers / IR retainer | Claim, support | Legal / risk | Per policy |

## Cadence and format
- Fixed update times (e.g. every 2 hours for Sev 1, twice daily for Sev 2), even when there is no news.
- Status update template:
```
Status as of 14:00 UTC: Contained / Investigating / Recovering
What changed since last update:
Current impact:
Next actions and owners:
Decisions needed:
Next update: 16:00 UTC
```
- Keep a single incident log (decisions with time and who decided).

## Out-of-band
If email, chat or identity may be compromised, move to a pre-arranged channel: separate
tenant chat, phone bridge, Signal group with verified members. Do not discuss the incident
in channels the attacker may monitor, and do not email the suspected compromised mailbox.

## Coordination rules
- One spokesperson externally; all external statements approved by legal and comms.
- Facts only, with confidence; never promise "no data was taken" until proven.
- Employees told what to do (report phishing, do not power off), not technical detail.

## Gotchas
- Forgetting third parties who run your systems (MSP, SaaS vendor) delays containment.
- Updates that change the story without explanation destroy trust; note what was corrected and why.
- Regulatory clocks start at awareness; legal must be in the loop from the first hour.

## Verify
- [ ] Contact list and out-of-band channel tested in the last tabletop.
- [ ] Every update in the incident log was sent on schedule.
