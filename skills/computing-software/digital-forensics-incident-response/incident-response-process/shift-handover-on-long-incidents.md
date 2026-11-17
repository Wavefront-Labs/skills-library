---
id: computing-software.digital-forensics-incident-response.incident-response-process.shift-handover-on-long-incidents
name: shift-handover-on-long-incidents
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [shift-handover, incident-commander, csirt, responder-fatigue, dfir]
level: practitioner
status: draft
description: "Run shift rotation and handovers on multi-day incidents: rota design, handover template, open-thread transfer and fatigue management."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://sre.google/sre-book/managing-incidents/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shift handover on long incidents

**Goal:** keep a multi-week incident moving 24x7 without losing threads or burning out the team.

## Rota design
- Decide within the first 24 h whether the incident needs follow-the-sun coverage; a team that
  has been up 30 hours makes containment mistakes.
- 12 h maximum shifts, overlapping by 30-60 min for handover.
- Each shift has a named shift lead (deputy IC) with decision authority defined in advance.
- Rest is enforced: the IC sends people home, including themselves (handing command over formally).

## Handover template (written, then spoken)
1. Current severity, phase, scope numbers.
2. Containment status and anything temporarily allowed that must be reversed.
3. Open analysis threads: question, owner, evidence location, next step.
4. Pending requests to third parties (retainer, cloud provider, law enforcement) and expected reply times.
5. Decisions made this shift (link to decision log).
6. Watch items: alerts to monitor, attacker activity windows, scheduled actions (password resets at 02:00).
7. Comms due: next exec update, regulator clock.

## Command transfer
- Explicit words: "I am handing incident command to X at 19:00 UTC"; X confirms and it is posted
  in the command channel and decision log.
- Outgoing IC stays reachable for 1 h.

## Gotchas
- Verbal-only handovers lose details; the next shift repeats work.
- Long-running jobs (Plaso, hunts, imaging) started without a note of where output goes.
- Times written in local time across time zones; use UTC everywhere.

## Verify
Each incoming lead can state every open thread and its owner without asking the previous shift.
