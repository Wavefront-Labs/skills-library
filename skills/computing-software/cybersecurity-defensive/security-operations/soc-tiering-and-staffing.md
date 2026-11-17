---
id: computing-software.cybersecurity-defensive.security-operations.soc-tiering-and-staffing
name: soc-tiering-and-staffing
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-management, soc-tiers, soc-staffing, tier-1, tier-2, tier-3, 24x7-coverage, analyst-burnout, mssp, mdr]
level: practitioner
status: draft
description: "Design SOC tiers and staffing: tier responsibilities, 24x7 headcount arithmetic, when to use an MDR/MSSP, and how to avoid analyst burnout."
sources: ["MITRE 11 Strategies of a World-Class Cybersecurity Operations Center (Strategies 2 and 4)", "SANS SOC Survey", "CySA+ CS0-003 objective 1.5"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC tiering and staffing

**Goal:** enough skilled people on every shift to meet response targets, with clear
responsibilities and a path that keeps analysts learning instead of leaving.

## Tier model
| Tier | Does | Does not |
|---|---|---|
| 1 Triage | Works the alert queue with runbooks, enriches, closes benign, escalates | Deep forensics, containment of production |
| 2 Incident response | Investigates escalations, scopes, contains with authority, coordinates IT | Long-running engineering |
| 3 Hunting / DFIR / detection engineering | Hunts, forensics, writes and tunes detections, automation | Queue work except during incidents |
| SOC manager / lead | Prioritisation, metrics, staffing, stakeholder comms | |
Many modern SOCs flatten tiers 1-2 with heavy automation; keep the responsibilities even if titles merge.

## 24x7 arithmetic
A single seat covered 24x7x365 = 8,760 hours. One full-time analyst works roughly
1,700-1,800 productive hours after leave, training and sickness. So **one seat needs about
5 analysts**; two seats on every shift need about 10, before managers and engineers.
If that headcount is not available, use an MDR/MSSP for out-of-hours with a clear
escalation contract, and keep in-house staff on business hours, engineering and IR.

## Working with an MDR/MSSP
- Contract: what they monitor, response targets, which actions they may take (isolate host? disable user?), escalation contacts, data retention, and exit (log and detection ownership).
- Weekly quality review of their escalations: false-escalation rate and missed detections.

## Burnout controls
- Rotate analysts between queue and project time (e.g. 60/40 for tier 1 after six months).
- Tune noisy detections relentlessly; alert fatigue is a retention problem.
- Limit consecutive night shifts and give recovery days after major incidents.
- Training budget and certification path (Security+, CySA+, GCIH, etc.) tied to tier progression.

## Gotchas
- Staffing to average alert volume fails during incidents; plan a surge roster.
- Single-person night shifts cannot handle a Sev 1 alone: on-call backup is mandatory.

## Verify
- [ ] Coverage calendar shows no unstaffed hours and a named backup for each shift.
- [ ] Queue SLA met during the busiest week of the last quarter.
