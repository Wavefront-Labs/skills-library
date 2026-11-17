---
id: transportation-logistics.traffic-transport-signalling.traffic-management-centre-operations.incident-detection-response-plans-and-vms-messaging
name: incident-detection-response-plans-and-vms-messaging
category: transportation-logistics
field: traffic-transport-signalling
product: traffic-management-centre-operations
tags: [traffic-management-centre, tmc, traffic-control-centre, rcc, toc, cctv, atms, incident-detection, congestion-management, response-plans, variable-message-signs, vms, dms, cms, traveller-information, 511, ramp-metering, lane-control-signals, smart-motorway, operator-log, shift-handover, situational-awareness]
level: practitioner
status: draft
description: "Running a road control-room shift: detecting incidents from CCTV and detectors, activating pre-approved response plans, and writing short, accurate VMS and traveller messages."
sources: ["FHWA Transportation Management Center Concepts of Operation guidance", "FHWA Changeable Message Sign Operation and Messaging Handbook", "National Highways (UK) public descriptions of regional operations centres"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident detection, response plans and VMS messaging

**Goal:** see problems on the network within minutes, apply the right pre-agreed
response, and tell drivers something short, true and useful.

## 1. Detect
- **Sources:** detector data (speed/occupancy alarms, automatic incident detection),
  CCTV patrol tours, emergency service and police calls, partner agencies, probe-data
  feeds (navigation apps), social media.
- Set a **CCTV tour** of known hotspots and rotate camera presets; return cameras to
  their home preset after use (a camera left pointing at a wall is a blind spot).
- A speed drop at one detector station with normal flow downstream = likely incident
  between stations; check the camera.
- **Verify** before acting (camera confirmation or two independent sources), but do
  not wait for perfect information on high-speed roads — queue-protection signs can go
  up on detection.

## 2. Respond with pre-approved plans
Response plans are scripted sets of actions per scenario/location: "lane 1 closed
between junctions 4 and 5" → lane control signals, VMS messages, signal plan changes,
notifications.
1. Open an incident record (time, location, lanes affected, source).
2. Select and activate the plan; tick each action as confirmed on the device status
   (not just sent).
3. Notify partners per plan: police, emergency services, recovery, maintenance,
   neighbouring control rooms, transit operators.
4. Update the record as the situation changes; escalate per thresholds (closures
   expected > X minutes, casualties, hazmat).
5. Close down: remove every sign and setting the plan activated — the most common
   failure is a stale "lane closed" message hours later.

## 3. Writing VMS messages
- Order: **what/where → effect → action**. e.g. "CRASH AT J5 / 2 LANES CLOSED /
  EXPECT DELAYS" or "ACCIDENT / A12 CLOSED / USE A14".
- Keep to the sign's lines and characters; drivers read ~1 phase at speed. Prefer one
  phase; two phases maximum.
- Use **standard abbreviations** from your national guidance only.
- Never show stale, vague ("CAUTION") or non-actionable messages; accuracy keeps
  drivers trusting signs.
- Travel-time messages only when the data feed is healthy.
- Diversion messages must match a planned, signed route with capacity.

## 4. Traveller information
- Update 511/web/app feeds and broadcast partners at the same time as signs.
- Give an expected duration only if you have a basis (recovery ETA, police estimate);
  otherwise say "until further notice".

## 5. Shift discipline
- Operator log: every action with time.
- Handover: open incidents, active plans and signs, faults (cameras, detectors, signs
  offline), planned works and events for the next shift.

## Gotchas
- Ramp metering and signal plans changed during incidents must be reverted.
- Secondary crashes in queues are common — activate queue-protection early.
- Privacy: don't record or share CCTV beyond policy; avoid zooming on people/plates
  unless operationally needed.
- *Message formats and abbreviation lists are jurisdiction-specific.*

## Verify
- [ ] Every activated device confirmed by status feedback, not assumed.
- [ ] Incident record has detection time, verification time, plan activation time and clearance time.
- [ ] VMS messages follow what/where → effect → action and fit one phase.
- [ ] At incident close, all signs and plan settings reverted and feeds updated.
