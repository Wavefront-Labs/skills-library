---
id: energy-mining-utilities.power-generation.control-room-operations.shift-turnover-and-abnormal-event-response
name: shift-turnover-and-abnormal-event-response
category: energy-mining-utilities
field: power-generation
product: control-room-operations
tags: [control-room-operations, power-generation, control-room, unit-operator, shift-supervisor, shift-turnover, shift-handover, panel-walkdown, watchkeeping, log-keeping, operator-log, alarm-response, alarm-flood, abnormal-operating-procedure, aop, emergency-operating-procedure, situational-awareness, standing-orders, out-of-service-equipment, lockout-register, human-performance, conduct-of-operations]
level: practitioner
status: draft
description: "Hand over and take over a power-plant control room shift, and handle an abnormal event: the turnover checklist, panel walkdown, log entries, alarm triage and the stabilise-then-diagnose order."
sources: ["EEMUA 191 alarm management guidance (principles)", "Industry conduct-of-operations practice (paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shift turnover and abnormal-event response

**Goal:** the oncoming crew knows exactly what state the plant is in before they take
responsibility, and when something goes wrong the crew stabilises first, diagnoses
second, and writes it down. These two habits prevent most avoidable control-room
events at any plant type — fossil, gas, hydro, nuclear or CHP.

## 1. Turnover — taking over the desk
Arrive early enough (often 15–30 minutes). In this order:
1. **Read the log** since your last shift: trips, equipment changes, alarms, phone
   instructions from dispatch, anything "awaiting".
2. **Status boards / registers:** equipment out of service, isolations and permits
   live, temporary modifications, defeated alarms or bypassed interlocks (each one
   should have an owner and an expiry), standing and night orders.
3. **Panel walkdown with the off-going operator:** go across every screen or panel —
   unit loads and limits, auxiliaries running vs standby, abnormal valve positions,
   standing alarms and why each is standing, trends that are drifting.
4. **Evolutions in progress:** what step, what's next, who's in the field. Avoid
   turning over mid-evolution; if you must, brief the exact step.
5. **Ask, don't assume:** "Anything you're worried about?" catches what the log
   doesn't.
6. Formal acceptance: "I have the watch" (or your site's phrase), time logged. Until
   then, the off-going operator is responsible.

## 2. Log keeping
- Timestamp, what happened, what you did, who told you. Facts, not opinion.
- Log every alarm you acknowledged without fixing, every instruction from dispatch
  (load set points, reactive requests), every field report.
- If it isn't in the log, the next shift doesn't know it.

## 3. Abnormal event — the order of work
1. **Recognise:** a trip, an alarm burst, an unexpected change on a trend.
2. **Stabilise:** take the immediate actions you are trained to take from memory
   (e.g. verify the unit tripped and fuel is off, confirm auxiliaries running, check
   drum level). Get the plant into a safe, steady condition.
3. **Announce:** tell the shift supervisor and the crew; one person coordinates.
4. **Enter the procedure:** abnormal/emergency operating procedure for the symptom.
   Read it, don't recite it.
5. **Diagnose** only once stable: what tripped first (first-out alarm, sequence of
   events record), what changed just before.
6. **Communicate outward:** dispatch/grid control on lost generation, environmental
   reporting if limits were exceeded, management per call-out list.

## 4. Alarm floods
When hundreds of alarms arrive in minutes:
- Don't acknowledge in bulk and lose the evidence — silence the horn, then work
  from **priority** (critical first) and the **first-out** list.
- Use the alarm summary sorted by time to find the initiating alarm.
- Assign one operator to watch the critical parameters while another works alarms.
- Afterwards: report nuisance and chattering alarms for rationalisation (see
  manufacturing-production.chemical-process-manufacturing.control-room-operation.alarm-floods-trends-and-shift-handover
  for a process-plant treatment of the same problem).

## Gotchas
- "It's always in alarm" is how real failures hide. Every standing alarm needs a
  reason on the board.
- Fatigue on nights: plan demanding evolutions for when the crew is fresh, and use
  peer checks for any manipulation.
- Phone calls during an event: one person takes them so the panel operator isn't
  distracted.
- Uncertain: turnover formats, immediate actions and reporting chains are site- and
  regulator-specific — this is the common pattern, not a procedure.

## Verify
- [ ] Log, registers and standing orders read before the walkdown.
- [ ] Every standing alarm and defeated interlock explained at turnover.
- [ ] Watch acceptance time logged.
- [ ] During an event: stabilised first, procedure entered, supervisor informed.
- [ ] First-out and sequence of events captured before resetting anything.
