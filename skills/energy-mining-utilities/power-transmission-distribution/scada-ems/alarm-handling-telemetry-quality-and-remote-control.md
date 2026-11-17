---
id: energy-mining-utilities.power-transmission-distribution.scada-ems.alarm-handling-telemetry-quality-and-remote-control
name: alarm-handling-telemetry-quality-and-remote-control
category: energy-mining-utilities
field: power-transmission-distribution
product: scada-ems
tags: [scada-ems, scada, ems, energy-management-system, adms, dms, control-room, alarm-handling, alarm-flood, alarm-priority, acknowledge, chattering-alarm, alarm-inhibit, telemetry, data-quality, quality-flags, stale-data, manual-override, substituted-value, rtu, ied, dnp3, iec-60870-5-104, iec-61850, state-estimator, residuals, select-before-operate, remote-switching, operating-tags, ge-vernova, siemens-spectrum, hitachi-network-manager, osi-monarch]
level: practitioner
status: draft
description: "Work a grid SCADA/EMS console well: triage alarm floods, read telemetry quality flags and stale data, cross-check with the state estimator, and operate devices remotely without wrong-device errors."
sources:
  - "General SCADA/EMS operating practice and ISA-18.2 / EEMUA 191 alarm-management principles, summarised; vendor-neutral"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alarm handling, telemetry quality and remote control in grid SCADA/EMS

**Goal:** see what is really happening on the network through SCADA, act on the
alarms that matter, and remotely operate the right device every time. Screens and
menus differ between vendors (GE, Siemens, Hitachi Energy, OSI and others); the
discipline below transfers. Your control-room procedures govern who may operate what.

## 1. Alarm triage
- **Read priority first, then time order.** Priority 1 (loss of supply, protection
  operated, breaker trip) before housekeeping (door open, heater fail).
- **Acknowledging is not clearing.** Ack means "I've seen it"; the condition stays
  until the field changes. Don't ack a page of alarms without reading them.
- **Alarm floods** (a storm, a bus fault): go to the event/sequence-of-events list
  filtered by station and look for the **first event** — usually a protection
  operation — which explains the rest. Use the network diagram to see what is de-
  energised rather than reading 300 consequential alarms.
- **Chattering alarms** (repeating on/off): note them and raise a defect; inhibit only
  per procedure, with a tag/note saying who, why and until when. An inhibited alarm
  nobody remembers is a hidden hazard.

## 2. Telemetry quality — trust but check
Every value carries quality flags; learn your system's symbols for:
- **Old / stale / not updated** — the RTU or comms link has stopped reporting. The
  value on screen is the *last known*, not current. Breaker states can be wrong.
- **Manually entered / overridden** — someone typed it. Check why and whether it's still true.
- **Substituted / estimated** — calculated, not measured.
- **Invalid / out of range / telemetry failure.**
If a station's comms fail, treat all its indications as unknown; ask field staff for
local readings before switching anything that depends on them.

## 3. Cross-check with the EMS
- The **state estimator** fits all measurements to a network model; large residuals
  on a point suggest a bad measurement (wrong CT ratio, sign reversal, stuck value) or a
  wrong breaker status in the model.
- Compare: do flows into a bus sum to roughly zero? Does a feeder show current while
  its breaker shows open? Contradictions like these find bad data fast.
- Contingency analysis output is only as good as the input; check it isn't running
  on a model with an unresolved topology error.

## 4. Remote control
1. Work from the approved switching schedule
   (`energy-mining-utilities.power-transmission-distribution.network-switching.writing-and-executing-a-switching-schedule`).
2. Navigate to the device via the station display, **read the device ID back
   against the schedule**, and check no operating tags (e.g. "do not operate", "men at
   work") are on it.
3. **Select-before-operate:** select the device; the system highlights it and asks for
   confirmation. Read the highlighted device's name again before executing.
4. Execute, then wait for the **status check-back** (open/closed indication change)
   and confirm analogue values react as expected (current goes to zero, voltage
   collapses on the dead section).
5. If no status change arrives within the timeout: **don't re-send blindly.** The
   command may have worked with indication failing. Check analogues; ask for field
   verification.
6. Place or update SCADA tags to mirror field locks and earths so no other operator
   can remotely close onto a worksite.

## 5. Shift handover
Hand over active alarms, inhibited points (and why), stale stations, manual
overrides, tags in place and switching in progress. Write it down.

## Verify
- [ ] First-cause event identified in any alarm flood; inhibits documented.
- [ ] Stale, manual and substituted values recognised before acting on them.
- [ ] Contradictions checked against estimator residuals or flow balance.
- [ ] Every remote operation: device ID read twice, select-before-operate, check-back confirmed.
- [ ] SCADA tags match field isolations; handover log complete.
