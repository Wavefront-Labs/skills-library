---
id: transportation-logistics.railway-signalling.computer-based-control-centres.workstation-signalling-and-ars-supervision
name: workstation-signalling-and-ars-supervision
category: transportation-logistics
field: railway-signalling
product: computer-based-control-centres
tags: [computer-based-control-centres, rail-operating-centre, roc, control-centre, signalling-workstation, vdu-signalling, cbi, computer-based-interlocking, ssi, westrace, smartlock, ars, automatic-route-setting, tms, traffic-management-system, etcs, ertms, cbtc, movement-authority, temporary-speed-restriction, alarm-handling, alarm-flood, signaller, train-describer, berth, headcode]
level: advanced
status: draft
description: "Signal from a computer-based workstation: supervise automatic route setting, intervene when it gets it wrong, manage ETCS/CBTC restrictions, and keep control during alarm floods."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workstation signalling and ARS supervision

**Goal:** run a large area from screens where most routes set themselves, while
staying ahead of the automation — knowing when to let it work and when to take over.

*Draft: products differ (various CBI and TMS suppliers, ETCS/CBTC systems). Command
names, alarm classes and screen layouts are system-specific; this is the workflow
common to them.*

## 1. Shift take-over
- Walk through each screen: trains in the area (train describer berths/headcodes),
  routes set, any routes or signals on manual, active TSRs and blocks/possessions,
  outstanding faults and alarms.
- Read the handover log; confirm with the outgoing signaller anything unusual:
  degraded working in force, ARS switched off anywhere, and why.

## 2. Supervising ARS (automatic route setting)
- ARS sets routes from the timetable and train describer. It does well with
  on-time trains and fails predictably with:
  - **out-of-course trains** (late, early, extra, wrong headcode),
  - **conflicts** where priority judgement is needed (see
    transportation-logistics.railway-signalling.signalling-regulation.junction-margins-and-train-priority),
  - **degraded areas** where routes need special handling.
- Look **two to three moves ahead** at each junction: what will ARS set next, and is
  it right? If not, take the signal/area off ARS (exclude it), set the route manually,
  then **restore ARS** — areas left on manual are a classic cause of later delays.
- Correct wrong headcodes/berths promptly; ARS decisions follow the describer.

## 3. ETCS / CBTC oversight
- Movement authorities are issued by the system; your job includes applying and
  removing **temporary speed restrictions** and emergency stops via the workstation.
- Double-check TSR entry (location from/to, speed, which tracks) with a second person
  or a read-back where required — an error here is a safety-critical data error.
- Know the fallback: what the system does if a train loses position or communication
  (often it degrades to staff-responsible / on-sight working with your authority).

## 4. Alarm handling
- Sort alarms by **safety relevance**, not arrival order: track occupied unexpectedly,
  points out of correspondence, level-crossing failures and emergency calls first;
  equipment health and communication warnings after.
- During an **alarm flood** (power dip, comms outage): stop issuing new authorities into
  the affected area, acknowledge in bulk only after reading, and phone the technical
  desk. Write down what you did and when.

## 5. Ergonomics that prevent errors
- Use the system's confirm/two-step commands deliberately; read back the object ID
  (signal number, points number) before confirming.
- Keep a manual notes pad for verbal authorities, messages and anything you're
  "keeping in your head".

## Gotchas
- ARS will happily route a late freight in front of an express — automation has no
  sense of consequence beyond its rules.
- Automation complacency: the quieter the screen, the more you need to scan.
- Commands sent to the wrong object because two IDs differ by one digit.

## Verify
- [ ] Take-over checklist done: manual areas, TSRs, possessions, faults confirmed.
- [ ] Every ARS exclusion has a reason and was restored afterwards.
- [ ] TSRs entered with read-back and checked on the overview.
- [ ] Safety alarms acknowledged only after action, with log entries.
