---
id: manufacturing-production.chemical-process-manufacturing.control-room-operation.alarm-floods-trends-and-shift-handover
name: alarm-floods-trends-and-shift-handover
category: manufacturing-production
field: chemical-process-manufacturing
product: control-room-operation
tags: [control-room-operation, board-operator, panel-operator, console-operator, dcs, process-operator, trend-reading, alarm-flood, alarm-management, isa-18-2, eemua-191, situational-awareness, field-operator, radio-communication, shift-handover, handover-log, grade-transition, upset, abnormal-situation-management, asm, first-out, closed-loop-communication, chemical-plant, refinery]
level: practitioner
status: draft
description: "Run a process unit from the board: scan trends, get through an alarm flood by finding the initiating event, direct field operators with closed-loop comms, and hand over a shift cleanly."
sources: ["EEMUA 191 alarm systems guide (general reference)", "ANSI/ISA-18.2 alarm management (general reference)", "ASM Consortium effective operator display and procedural practices (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control room operation: trends, alarm floods and handover

**Goal:** keep the unit inside its operating window from the board, catch drift
before it alarms, survive an alarm flood without losing the plot, and hand over so the
next shift isn't surprised.

## 1. The routine scan (every 15–30 minutes, and after any change)
1. **Overview display** first: unit-wide KPIs (feed rate, key temperatures, levels,
   product quality analysers). Look for anything off its normal mark — good overview
   displays grey out normal and colour only the abnormal.
2. **Trends** on the key variables at two timescales: last hour (is it moving now?)
   and last 8–24 hours (is it drifting slowly?). A level creeping 2% per hour will not
   alarm for hours but is already telling you a balance is off.
3. **Controllers:** anything in MAN that should be in AUTO? Any valve output pinned
   at 0% or 100% (saturated — control is lost even though the PV looks fine)?
4. **Standing alarms and shelved alarms:** still valid?

Trend-reading tells: an oscillation with constant period across several loops is
usually one loop's tuning or a sticky valve propagating; a step in one transmitter
alone with no process consequence is usually instrument.

## 2. Alarm flood: the method
More than ~10 alarms in 10 minutes per operator is a flood (EEMUA/ISA guidance); you
cannot process each one.
1. **Silence, don't mass-acknowledge.** Acknowledging everything erases the cue of what
   came first.
2. **Find the initiating event:** earliest alarms in the event journal, a first-out
   indicator on a trip, or the obvious cause (pump trip, power dip, feed loss).
3. **Make it safe first:** follow the abnormal or emergency procedure for that event —
   cut feed, put the unit to a safe holding state. Stabilise, then optimise.
4. **Use the priorities:** urgent/high alarms tied to safety limits come before quality
   or equipment-health alarms.
5. **Call for help early:** a second board operator or supervisor to take comms frees you
   to control.
6. Afterwards, log the sequence and raise any alarm that was useless during the flood
   for rationalisation.

## 3. Directing field operators
- Use **closed-loop communication**: you give the instruction with tag number and
  action ("Close FV-201 bypass, valve HV-201B"), they repeat it back, you confirm,
  they report when done, you confirm the result on the board.
- Ask for what you cannot see: local gauges, sight glasses, noise, smell, leaks, pump
  vibration. Field confirmation is how you separate instrument faults from real ones.
- Never send someone into an area with an active toxic or flammable alarm without the
  site's response procedure.

## 4. Transitions (startup, rate change, grade change)
- Move one thing at a time and wait for the response — time constants on big plant are
  minutes to hours. Write the plan with target values and hold points before starting.
- Pre-stage: know which alarms will legitimately fire and which would be real. Some
  sites use state-based alarming; if not, brief the team.

## 5. Shift handover
Written log plus a face-to-face walk-through at the board, covering:
- Current state vs plan (rates, grades, targets) and anything abnormal.
- Loops in MAN, bypassed interlocks, overrides, shelved/suppressed alarms — each with
  reason and who authorised it.
- Equipment out of service, permits open in the field, work in progress.
- What to watch: the slow drift, the transition due in four hours.
The incoming operator should read back the key points. Handover failures feature in
many major accident investigations.

## Gotchas
- A valve at 100% with PV on setpoint is not "fine": you have no margin left.
- An operator who never takes manual control loses the feel for the unit; practise
  on simulators where available.
- "It always does that" is how normalised deviance starts. Log it, raise it.

## Verify
- [ ] You can name the 5–10 variables that tell you the unit is healthy and their normal ranges.
- [ ] No controller saturated or in MAN without a recorded reason.
- [ ] In a flood you identified the first event before acknowledging the bulk.
- [ ] Field instructions were repeated back and confirmed.
- [ ] Handover covered overrides, bypasses, shelved alarms and open permits.

*Draft note:* flood threshold and scan intervals are typical guidance figures; your
site's alarm philosophy sets the actual numbers.
