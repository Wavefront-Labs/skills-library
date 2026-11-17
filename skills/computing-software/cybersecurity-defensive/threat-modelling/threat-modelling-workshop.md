---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-modelling-workshop
name: threat-modelling-workshop
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling-process, threat-modelling-workshop, facilitation, elevation-of-privilege-card-game, stride, whiteboard, collaborative-threat-modelling]
level: practitioner
status: draft
description: "Facilitate a threat modelling workshop: who to invite, preparation, a timed agenda around the DFD and STRIDE, capturing threats and agreeing actions."
sources: ["Threat Modeling Manifesto", "Adam Shostack - Threat Modeling: Designing for Security (Wiley 2014)", "Microsoft Elevation of Privilege card game", "OWASP Threat Modeling Cheat Sheet"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a threat modelling workshop

**Goal:** in a few hours, the people who build the system find the threats that matter and
leave with owned actions.

## Invite
Engineers who know the code and infrastructure (2-4), product owner, an architect, a
security facilitator, and an operations/SRE person. Keep it under 8 people.

## Prepare (facilitator, before the session)
- Draft a data flow diagram from design docs; mark trust boundaries; share 2 days ahead.
- Collect: data classification, user roles, external dependencies, existing controls.
- Decide scope: one feature or service per session.

## Agenda (3 hours)
| Time | Activity |
|---|---|
| 0:00 | Purpose, scope, ground rules (no blame, all ideas captured) |
| 0:10 | Walk the DFD; team corrects it (this alone finds issues) |
| 0:40 | Threat elicitation per trust boundary crossing with STRIDE prompts; or play Elevation of Privilege cards to keep everyone engaged |
| 1:50 | Break |
| 2:00 | Group and rate threats (likelihood x impact, or simple high/medium/low) |
| 2:30 | For high and medium threats: existing control? gap? proposed mitigation, owner |
| 2:50 | Recap actions, next steps, when to revisit |

## Facilitation techniques
- Ask "how would you break this?" to engineers about their own component.
- Use concrete attacker goals ("read another tenant's invoices") to focus.
- Park out-of-scope topics visibly.
- Capture threats as statements: "An attacker with a stolen session token can call the admin API because it does not check role" (actor, action, asset, reason).

## Output
Threat list with IDs, ratings, mitigations, owners and tickets; updated DFD; assumptions and
accepted risks. Publish within 2 days.

## Gotchas
- Without engineers who know the system, the session produces generic threats.
- Spending 2 hours on the diagram leaves no time for threats: prepare it.
- Ratings debates: timebox; the action matters more than the score.

## Verify
- [ ] All high threats have tickets in the team backlog.
- [ ] Participants rate the session useful (quick survey) and the next model is requested, not imposed.
