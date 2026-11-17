---
id: energy-mining-utilities.water-treatment-supply.water-scada-telemetry.telemetry-alarm-triage-and-remote-pump-control
name: telemetry-alarm-triage-and-remote-pump-control
category: energy-mining-utilities
field: water-treatment-supply
product: water-scada-telemetry
tags: [water-treatment-supply, water-scada-telemetry, scada, telemetry, outstation, rtu, plc, hmi, alarm-triage, alarm-flood, comms-failure, remote-control, pump-control, valve-control, trend-analysis, data-logger, flow-logger, pressure-logger, control-room, water-control-centre, alarm-acknowledge, operator, ot-security]
level: practitioner
status: draft
description: "Triage water SCADA/telemetry alarms: separate comms faults from real events, read trends, operate pumps and valves remotely safely, and dispatch with the right info."
sources:
  - "ISA-18.2 / EEMUA 191 alarm management concepts, paraphrased"
  - "Water utility control-room operating practice as commonly taught, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Telemetry alarm triage and remote pump control

**Goal:** in a water control room, decide quickly which alarms mean water is (or soon will
be) not reaching customers or not safe, act remotely where that is safe, and send the right
person with the right information.

This is tool-agnostic: the same logic applies whether your system is a large SCADA suite or
a cloud telemetry portal for loggers.

## 1. First look: is the data real?
For any alarm, check in this order:
1. **Comms status** of the outstation/RTU — "comms fail", stale timestamp, or all values
   frozen flat means you're looking at old data. Many "level low" alarms are actually
   instrument or comms faults.
2. **Instrument sanity** — a level jumping 0→100% instantly, negative flows, or a value
   pinned at range limit points to a sensor or 4–20 mA loop fault.
3. **Corroborate** with a second signal: reservoir level vs outlet flow vs downstream
   pressure; pump "running" status vs motor current vs flow.

## 2. Prioritise by consequence
Rank by what happens next, not by alarm order:
- **Water quality / public health:** chlorine residual low/high at works or reservoir
  outlet, turbidity high on treated water, dosing pump fail. Act first.
- **Loss of supply:** reservoir falling with inlet pump tripped; trunk main pressure collapse
  (possible burst).
- **Imminent environmental/property damage:** overflow, flooding at a site.
- **Asset protection:** pump high temperature, high vibration.
- **Nuisance:** door/intruder alarms (still check — sabotage and theft happen), power
  blips that self-cleared.
In an alarm flood (e.g. storm or power cut), work by site and consequence; don't simply
acknowledge everything.

## 3. Read the trend before acting
Pull 24–72 h of trends: is this a step (trip, burst), a ramp (demand, slow leak), or a
cycle (control band too tight)? Compare to the same weekday last week. A pressure drop
with flow increase on a district meter at night is a classic burst signature.

## 4. Remote control safely
- Confirm the site is not in **local/hand** mode and no one is on site working (permit
  board/log) before starting a pump or moving a valve remotely.
- Reset a trip **once**; if it trips again, send someone — repeated resets burn motors.
- Open/close remote valves slowly or in steps; watch downstream pressure for surges.
- Change setpoints only within approved limits; log every manual intervention with
  reason, time and your name, and return to auto when done.

## 5. Dispatch well
Give the field team: site, alarm, time it started, what trends show, what you've tried
remotely, current state (pump in auto/off, valve %), safety notes (lone working, access).

## 6. Logger data
For battery data loggers (pressure, flow, noise), check last-call-in time and battery; a
logger that stops calling in is a gap in compliance or leakage data — raise a job.

## Gotchas
- Acknowledging an alarm does not fix it; standing alarms get ignored — challenge chronic
  nuisance alarms through alarm review.
- Timestamps in outstation local time vs server UTC cause confusion around clock changes.
- Remote access tooling is an OT security risk; use only approved access paths.

## Verify
- [ ] Data freshness and comms checked before acting on any value.
- [ ] Quality and supply alarms handled before asset/nuisance alarms.
- [ ] No remote operation on a site with people working or in local mode.
- [ ] Every manual intervention logged and returned to auto.
- [ ] Dispatch note includes trend summary and current state.

*Uncertain:* alarm priorities and remote-operation permissions are set by each utility's
control philosophy.
