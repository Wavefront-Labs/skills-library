---
id: computing-software.digital-forensics-incident-response.incident-response-process.ir-roles-and-raci
name: ir-roles-and-raci
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ir-raci, incident-roles, incident-commander, roles-and-responsibilities, ir-plan, dfir]
level: practitioner
status: draft
description: "Define incident response roles and a RACI so every decision (isolate, notify, pay, disclose) has exactly one accountable owner and named deputies."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.fema.gov/emergency-managers/nims/components"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IR roles and RACI

**Goal:** no decision during an incident waits because nobody knows who owns it. NIST SP
800-61r3 lists leadership, IR team, technology, legal, PR, HR, physical security and third
parties as role holders; the Incident Command System (NIMS/ICS) supplies the command model.

## Core roles
| Role | Does | Must not |
|---|---|---|
| Incident commander (IC) | Owns the response, sets objectives and cadence, makes or escalates decisions | Do hands-on analysis |
| Technical lead | Directs investigation and containment work | Brief execs ad hoc |
| Scribe | Keeps the decision log and timeline | Be skipped "because it's small" |
| Comms lead | Drafts internal and external messages | Release anything legal has not seen |
| Legal counsel | Privilege, notification duties, law enforcement | Direct the technical work |
| Exec sponsor | Business risk decisions (shut down a revenue system, ransom) | Join every bridge |
| HR | Employee-involved cases | |
| System owners | Approve downtime, validate recovery | |

## RACI for decisions (R does, A single owner, C consulted, I informed)
| Decision | IC | Tech lead | Legal | Exec | Comms | System owner |
|---|---|---|---|---|---|---|
| Declare incident / set severity | A | R | I | I | I | I |
| Isolate a production system | A | R | I | C | I | C |
| Reset all domain credentials | A | R | I | C | I | C |
| Engage outside IR firm | R | C | A | C | | |
| Notify regulator / customers | C | C | A | C | R | |
| Contact law enforcement | C | | A | C | | |
| Ransom payment decision | C | C | C | A | | |
| Public statement | I | C | C | A | R | |

Rule: exactly **one A per row**. Two As means a stalled decision.

## Practicalities
- Name a primary and **two deputies** per role; incidents outlast one person's shift.
- Pre-authorise thresholds: the IC may isolate any non-production host without asking;
  production needs the system owner *consulted*, not *approving*.
- Shift hand-over checklist: open actions, pending decisions, current hypotheses, next sync.
- Put the RACI in the plan annex and in the case template so it is on screen during the bridge.

## Verify
In a tabletop, pick five decisions at random and ask "who decides?". Answers must match the
RACI without discussion.
