---
id: repair-maintenance.facilities-maintenance.maintenance-rounds-inspection.daily-building-rounds-plant-readings-and-defect-escalation
name: daily-building-rounds-plant-readings-and-defect-escalation
category: repair-maintenance
field: facilities-maintenance
product: maintenance-rounds-inspection
tags: [maintenance-rounds-inspection, building-rounds, daily-rounds, walkround, plant-room-checks, meter-readings, log-sheet, boiler-pressure, chiller, pump-check, water-temperature, legionella, defect-logging, defect-reporting, escalation, fire-panel, sprinkler-gauge, fire-exit-check, housekeeping, qr-code-checklist, mobile-inspection, cmms]
level: practitioner
status: docs-checked
description: "Design and walk daily building rounds: route and checklist, plant room readings with limits, spotting defects early, CMMS logging and escalation judgement."
sources:
  - https://www.hse.gov.uk/legionnaires/hot-and-cold.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daily building rounds, plant readings and defect escalation

**Goal:** catch problems while they are cheap — a weeping pump seal, a propped fire
door, a pressure drifting low — by walking a fixed route with a checklist, recording
readings against limits, and escalating the right things at the right speed.

## 1. Design the route
1. Start from the riskiest spaces: plant rooms, fire panel, risers, roof plant,
   kitchens, washrooms, escape routes, car park, perimeter.
2. Sequence a loop with no backtracking; split into morning and afternoon loops if
   the building is large.
3. Place a QR/NFC tag at each checkpoint so a mobile CMMS or inspection app
   timestamps the visit and opens the right checklist.
4. Vary the start point occasionally so the same areas aren't always seen at the
   tail end when attention drops.
5. Revisit the route each quarter and after building changes.

## 2. What to check (example checklist)
**Plant room (read and record, don't just glance):**
- Heating system pressure (record the design value on a label at the gauge).
- Flow/return temperatures; hot water stored at least 60 °C and reaching 50 °C (55 °C in
  healthcare premises) within 1 minute at outlets, cold water below 20 °C where possible,
  where temperature is the Legionella control (HSE guidance, UK; other jurisdictions
  differ, so follow your local water-hygiene plan).
- Pumps: duty running, standby available, no new noise/vibration, seals dry, no
  hot motor smell.
- Leaks, drips, pooling, corrosion staining, alarms on BMS/controls panels.
- Sprinkler valve set gauges and valve positions (strapped/locked open).
- Meters: electricity, gas, water — same time each day so consumption is comparable.
**Building:**
- Fire alarm panel: normal, no faults or disablements left on.
- Escape routes clear, exit doors open freely, fire doors closing and not wedged,
  exit signs and emergency lights' status LEDs green.
- Lighting out, ceiling tiles stained or missing (leaks), trip hazards, damaged
  floors, broken glass, graffiti, pest signs.
- Washrooms: leaks, running urinals, blocked fixtures, consumables.
- External: roof drains and gutters, security fencing, lighting, signs of intrusion.

## 3. Readings need limits
For each reading record normal range and action limits on the checklist, e.g.
"Heating pressure: normal [design range]; below [action limit] raise a work order; below
[lower limit] call supervisor", with limits from the plant manual. A reading without a limit is a number nobody acts on. Trend daily meters:
a water meter rising overnight with the building empty means a leak.

## 4. Logging defects
Every defect becomes a work order with: location/asset ID, what you saw (not what you
assume), photo, risk, and any make-safe done. One defect, one WO. Close the loop:
check last week's raised defects on the next round and chase stale ones.

## 5. Escalation judgement
| Level | Examples | Action |
|---|---|---|
| Immediate (stop and act) | Fire panel fault/disablement, blocked escape route, water near electrics, gas smell, sprinkler valve closed, injury risk | Make safe now, call supervisor/duty manager, follow emergency procedure |
| Same day | Plant on standby only, pressure below action limit, no hot water, major leak contained | Raise P1/P2 WO, phone the supervisor |
| Planned | Minor drips, lamps out, cosmetic damage | Raise WO, normal priority |
Gas smell: follow your site's gas-leak emergency procedure and call the gas emergency number from a safe place.

## Gotchas
- "Tick-box blindness": insist on recorded values, not ticks.
- Ignoring a slowly trending value until it trips is the classic miss — look at the
  last 7 days, not just today.
- Lone working in plant rooms and roofs needs a check-in system.
- Don't silence or reset fire panel faults unless you are trained and authorised.

## Verify
- [ ] Every checkpoint scanned with a timestamp.
- [ ] All readings recorded as values and compared with limits.
- [ ] Each defect has a WO with photo and location.
- [ ] Immediate-level items escalated by phone, not only by ticket.
- [ ] Previous round's open defects reviewed and chased.

## Checked

Date checked: 2026-11-01. Jurisdiction: United Kingdom for the water-temperature figures (HSE).
Confirmed on the HSE hot and cold water systems page: hot water stored at least 60 °C, reaching 50 °C (55 °C healthcare) within 1 minute at outlets, cold water below 20 °C where possible.
Removed as unconfirmed: 45-90 minute route length, 1-1.5 bar sealed system pressure, 1.2-1.8/1.0/0.7 bar example limits, 50 °C return requirement, ASHRAE 188 reference, the gas-smell step list.

Method: documentation only; no commands were run.
