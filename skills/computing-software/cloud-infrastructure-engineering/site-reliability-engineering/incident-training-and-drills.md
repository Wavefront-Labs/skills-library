---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-training-and-drills
name: incident-training-and-drills
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [incident-training, incident-drills, incident-management, incident-command-system, tabletop-exercise, wheel-of-misfortune]
level: practitioner
status: docs-checked
description: "Train people for incident response: ICS role practice, Wheel of Misfortune, failure-injection exercises led by a trainee IC, time-bound simulation games and DiRT drills."
sources: ["https://sre.google/workbook/incident-response/", "https://sre.google/sre-book/being-on-call/", "https://sre.google/sre-book/managing-incidents/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident training and drills

Workbook "Incident Response": Google's incident response is based on the Incident Command System (ICS),
established in 1968 by firefighters; Incident Management at Google (IMAG) and PagerDuty's process are
two adaptations. Train people on the framework and its roles before real incidents.

## Roles to practise
Incident Commander (IC), Communications Lead (CL) and Operations Lead (OL). The CL and OL report to the IC.
The person who declares the incident typically becomes IC; by default the IC holds every role not yet
delegated, and may hand the role off. The IC can hand over command to someone more experienced with the
framework (the GKE case study does this). If an incident shrinks, the CL role can fold back into the IC.

## Drill formats the sources describe
| Format | Source description |
|---|---|
| Wheel of Misfortune | team exercise that sharpens troubleshooting and service knowledge (SRE Book, On-Call chapter; detail is in Accelerating SREs to On-Call) |
| Failure injection led by a trainee IC | PagerDuty's weekly Failure Friday: a person training to be IC acts as a real IC while experts use real incident vocabulary and processes |
| Time-bound simulation games | PagerDuty uses games with time pressure (it names "Keep Talking and Nobody Explodes") to reproduce urgency that failure injection cannot |
| Company-wide disaster exercise | Google's annual DiRT (Disaster Recovery Training) mixes theoretical and practical drills in multiday tests of infrastructure and services |
| Review of past incidents | PagerDuty reviews postmortems and records major-incident calls to learn from them |

## Gotchas
- Rotate who plays IC so skill spreads past senior engineers (a design choice; the Workbook shows trainees
  acting as IC in drills).
- Failure injection alone does not reproduce the urgency of a major incident; add time pressure.

## Verify
- [ ] Every on-call engineer has practised at least one incident role in a drill.
- [ ] Past incidents and drill findings feed the next exercise.

## Checked
2026-11-01. Confirmed against the SRE Workbook Incident Response chapter (ICS, roles, Failure Friday,
simulation games, postmortem review) and the SRE Book On-Call chapter (Wheel of Misfortune, DiRT). Removed:
the 1 h and half-day durations, the six-month readiness metric, the tabletop script (invented scenario),
planning lead and scribe roles, and the quarterly calendar, none of which those pages state.
Method: documentation only; no commands were run.
