---
id: repair-maintenance.building-services-equipment-maintenance.building-automation-systems.bms-alarm-triage-and-point-troubleshooting
name: bms-alarm-triage-and-point-troubleshooting
category: repair-maintenance
field: building-services-equipment-maintenance
product: building-automation-systems
tags: [building-services-equipment-maintenance, building-automation-systems, bms, bas, bems, ems, niagara, tridium, niagara-4, metasys, johnson-controls, desigo, siemens, bacnet, modbus, lonworks, alarm-triage, nuisance-alarms, point-troubleshooting, sensor-calibration, overrides, operator-override, schedules, setpoints, trend-logs, pid-loop, hunting, facilities]
level: practitioner
status: draft
description: "Triage BMS/BAS alarms, trace a bad point from graphic to field device (sensor, wiring, controller, BACnet), clear stale overrides, tune schedules and use trends to prove a fix."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BMS alarm triage and point troubleshooting

**Goal:** turn a noisy alarm list into action, find out whether a "bad" value is the
plant, the sensor, the wiring or the controller, and prove the fix with trends. Applies to
Tridium Niagara 4 (and the many OEM brands built on it), JCI Metasys and Siemens Desigo;
menu names differ but the method doesn't.

## 1. Triage the alarm list (start of shift)
1. Sort by **priority**, then by **count/time**: life-safety and critical plant
   (chiller trip, boiler lockout, freeze stat, server room high temp, sump high level)
   first.
2. Group duplicates: one failed controller can raise dozens of "offline" or out-of-range
   alarms. Fix the root (comms, power) first.
3. For each real alarm: acknowledge, write the action in the alarm note, assign.
4. Weekly: list the **top 10 repeat alarms**. Nuisance alarms (a limit set too tight, no
   delay, alarming in unoccupied mode) train operators to ignore real ones — fix the
   alarm setup (deadband, delay e.g. 5–15 min for temperatures, occupancy inhibit), and
   record why.

## 2. Find stale overrides
Overrides ("operator", "manual", "out of service", Niagara priority-8 "override",
Metasys "Operator Override", Desigo "manual" priority) are the most common reason plant
runs 24/7 or fails to respond. Run a report/filter of points in override, note who set it
and why, release those nobody can justify. Agree a rule: every override gets a note and
an expiry.

## 3. Troubleshooting a point, graphic → field
1. **Graphic vs point:** read the point directly in the controller (property sheet /
   point focus). A graphic bound to the wrong point is common after edits.
2. **Status flags:** fault, stale, down, out of service, overridden — they explain most
   odd values. "Stale/down" = comms problem, not sensor.
3. **Comms:** controller online? BACnet MS/TP trunk: check the device count online,
   termination at both ends only, shield grounded at one end, polarity, duplicate MAC
   addresses, baud mismatch. BACnet/IP: ping the device, check IP/BBMD for other subnets.
4. **Sensor:** compare with a calibrated reference at the sensor location (handheld
   thermometer/RH meter). Check input type set in the controller: 10k thermistor type
   II vs type III, 1k Pt RTD, 0–10 V, 4–20 mA. Wrong type = plausible-looking wrong value.
5. **Wiring:** with the input disconnected, measure resistance at the sensor
   (10k thermistor ≈ 10 kΩ at 25 °C, higher when colder) or the mA loop current. Open
   circuit reads as extreme low/high; short reads the opposite extreme.
6. **Outputs:** command the output (with permission and safely), verify at the device:
   damper or valve actually strokes 0–100%, the relay energises. Feedback ≠ command means
   a stuck actuator, a linkage slip, or a missing auto/manual switch position on the
   panel (HOA left in Hand/Off).

## 4. Loops that hunt
A valve or damper oscillating every few minutes: check the actuator first (sticking,
backlash), then reduce gain / increase integral time; confirm the sensor isn't placed
where it sees the actuator's own effect too quickly. Trend before and after.

## 5. Schedules and setpoints
Check holiday calendars are loaded for the year, daylight-saving handled, optimum
start enabled and occupied hours match real use. Setpoint creep (users nudging limits)
is visible in trends — reset to the design/agreed values and lock if policy allows.

## 6. Prove it with trends
Set or check trend logs at 5–15 minute intervals for the point, its setpoint, the
output and any related points (e.g. supply air temp, valve %, fan status). A fix isn't
done until a day's trend looks right.

## Gotchas
- Never release a life-safety-related override without knowing why it was set.
- Editing logic or wiresheets live on a running plant: back up the station/database
  first (Niagara station backup, Metasys archive) and follow the change procedure.
- Keep credentials out of shared notes; BMS networks are a security target — default
  passwords must be changed.

## Verify
- [ ] Critical alarms addressed and noted; repeat-alarm list reviewed.
- [ ] Override report clean or every override justified with an expiry.
- [ ] Faulty point traced to a cause (graphic / comms / sensor / wiring / output).
- [ ] Sensor reading matches a reference within tolerance (e.g. ±0.5 °C).
- [ ] Trend for 24 h shows stable control after the fix; backup taken before changes.
