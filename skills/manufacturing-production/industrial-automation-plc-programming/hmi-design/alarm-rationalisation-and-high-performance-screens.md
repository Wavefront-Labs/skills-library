---
id: manufacturing-production.industrial-automation-plc-programming.hmi-design.alarm-rationalisation-and-high-performance-screens
name: alarm-rationalisation-and-high-performance-screens
category: manufacturing-production
field: industrial-automation-plc-programming
product: hmi-design
tags: [hmi-design, hmi, scada, operator-interface, high-performance-hmi, isa-101, isa-18-2, iec-62682, eemua-191, alarm-management, alarm-rationalisation, alarm-philosophy, alarm-flood, nuisance-alarms, chattering-alarms, standing-alarms, alarm-priority, alarm-shelving, grey-screens, colour-discipline, situational-awareness, screen-hierarchy, level-1-overview, analog-indicators, trends, navigation, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Design operator screens and alarms that work under pressure: ISA-101 grey displays, four-level hierarchy, colour discipline and ISA-18.2 alarm rationalisation with targets."
sources: ["ISA-101.01 Human Machine Interfaces for Process Automation Systems", "ANSI/ISA-18.2 / IEC 62682 Management of Alarm Systems", "EEMUA 191 Alarm Systems guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alarm rationalisation and high-performance HMI screens

**Goal:** screens that let an operator see "normal vs abnormal" at a glance, and an
alarm system where every alarm means "act now" — independent of SCADA vendor.

*Draft: paraphrases ISA-101, ISA-18.2/IEC 62682 and EEMUA 191 principles; the
numeric targets are the widely quoted guidance values, not hard limits — set your
own in an alarm philosophy document.*

## 1. Screen principles (high-performance HMI)
- **Grey background, muted equipment, colour only for abnormal.** If a running pump
  is bright green and a stopped one red, the screen is a Christmas tree in normal
  operation and an alarm is invisible. Running/stopped are states — show them with
  fill/outline in greys; reserve saturated colour for alarms.
- **Reserve alarm colours** (e.g. red = priority 1, yellow/orange = 2, …) and use them
  for *nothing else* — not for buttons, not for "hot" pipes.
- **Never colour alone:** add shape or text (an alarm indicator with priority number
  and shape), because ~8% of men have red-green colour deficiency.
- **Show values in context:** analog bar indicators with the normal range shaded, and
  small trends next to key values. "73.2" means nothing; "73.2 in a 60–80 band,
  rising" means something.
- No 3D pipes, no animated flames, no photos of equipment.

## 2. Hierarchy and navigation
- **Level 1 — area overview:** the whole area of responsibility on one screen, KPIs
  and deviations; mostly trends and indicators, few numbers.
- **Level 2 — unit control:** the screen used for normal operation of one unit.
- **Level 3 — detail:** one piece of equipment, all its parameters.
- **Level 4 — diagnostics/help:** interlock status, procedures, device diagnostics.
- Any screen reachable in ≤3 clicks; consistent location for navigation and alarm
  banner on every screen. Show **why** a device won't start (interlock list), not just
  that it won't.

## 3. Alarm philosophy and rationalisation
An alarm is an indication of an abnormal condition **requiring a timely operator
response**. For each candidate alarm, a rationalisation team (operations, process,
controls) records:
1. **Cause**, **consequence if ignored**, **operator action**, **time available to act**.
2. No operator action → it is not an alarm (make it an event/log entry).
3. **Priority** from consequence severity × time to respond (a matrix in the philosophy).
4. **Setpoint**, **deadband** and **on/off delays** to stop chattering.
5. Who can **shelve** it, for how long, and how shelved alarms are reviewed.

Target distribution often cited: roughly 80% low / 15% medium / 5% high priority.

## 4. Measure it
Benchmark values commonly quoted (ISA-18.2/EEMUA 191):
- ~1 alarm per 10 minutes per operator in steady operation is "very likely acceptable";
  >1 per minute is overloaded.
- **Flood:** >10 alarms in 10 minutes per operator.
- Top-10 most frequent alarms usually produce a large share of the load — fix those first.
- Standing (stale) alarms > 24 h: review each; most are disabled equipment or wrong setpoints.

## 5. Alarm flood control
- **State-based alarming:** suppress alarms that are expected in a mode (e.g. low flow
  alarms while the line is stopped).
- **First-out / root-cause grouping** for trips: show the initiating cause, suppress
  the consequential cascade.

## Gotchas
- Vendor default object libraries are often colourful; build a greyscale library once.
- Every alarm added "just in case" is a tax on every future incident.
- Operators must be part of the design; test screens with them on a real upset scenario.

## Verify
- [ ] With the plant normal, the Level 1 screen shows almost no saturated colour.
- [ ] Every configured alarm has a documented cause, consequence and action.
- [ ] Average alarm rate and flood count are reported monthly.
- [ ] No alarm colour is reused for non-alarm meaning.
- [ ] Shelved and standing alarms are reviewed on a schedule.
