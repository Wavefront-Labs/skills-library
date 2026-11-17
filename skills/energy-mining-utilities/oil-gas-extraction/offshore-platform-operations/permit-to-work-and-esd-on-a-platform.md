---
id: energy-mining-utilities.oil-gas-extraction.offshore-platform-operations.permit-to-work-and-esd-on-a-platform
name: permit-to-work-and-esd-on-a-platform
category: energy-mining-utilities
field: oil-gas-extraction
product: offshore-platform-operations
tags: [offshore-platform-operations, offshore, platform, fpso, production-platform, control-room-operator, process-technician, permit-to-work, ptw, isolation, lockout-tagout, simops, toolbox-talk, process-train, separator, compressor, esd, emergency-shutdown, psd, process-shutdown, blowdown, fire-and-gas, f-and-g, muster, lifeboat, temporary-refuge, helideck, crane-operations, shift-handover]
level: practitioner
status: draft
description: "Work an offshore production platform shift: permit-to-work and isolation discipline, process train watch, ESD/PSD levels and response, muster, and the shift handover that holds it together."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Permit-to-work and ESD on a platform

**Goal:** keep the process running and people safe on an installation where everything
is close together: control work through permits and isolations, and respond correctly
when the shutdown system acts.

> Status: draft. Generic; each installation's safety case, permit-to-work system,
> cause-and-effect charts and emergency response plan govern. Terms differ slightly
> between operators.

## 1. Permit-to-work (PTW)
- Every non-routine job has a permit describing the **work, location, hazards,
  isolations, gas tests, controls and who is responsible**. Hot work, confined
  space, breaking containment, and work on safety-critical equipment typically need
  the highest level of permit.
- **SIMOPS:** the area authority checks for conflicting permits — e.g. hot work near a
  line being opened. Many incidents come from two "safe" jobs interacting.
- **Isolation:** positive isolation (spades/blinds or double block and bleed for process;
  electrical isolation with locks) verified by a second person, with each isolation
  point listed on an isolation certificate. Prove zero energy before breaking
  containment.
- **Gas test** for hot work and confined space, repeated at the set interval.
- Hand back: the job's site is inspected, isolations removed in a controlled order, and
  the equipment reinstated and leak-tested before returning to service.

## 2. Process watch
- Control room operators watch levels, pressures, temperatures and flows across the
  train (separators, compression, dehydration, water treatment). Field operators do
  rounds: walk-by checks for leaks, vibration, abnormal noise and smells, and verify
  local gauges against the control room.
- Track **produced water** quality against the overboard discharge limit (oil-in-water)
  — it is a regulatory parameter, not just a process one.
- Alarm management: acknowledge, understand, act. Standing alarms that everyone
  ignores mask new ones; report them for repair.

## 3. Shutdown levels
Typical hierarchy (names vary):
- **PSD (process shutdown):** a unit or train trips on a process upset; the rest of the
  platform runs.
- **ESD (emergency shutdown):** isolates the installation's inventory — closes
  emergency shutdown valves on risers and between sections.
- **Blowdown/depressurisation:** opens blowdown valves to send inventory to the flare.
- **Abandon platform shutdown** at the highest level.
Fire and gas (F&G) detection initiates actions according to the **cause-and-effect
charts**. Learn which detector votes trigger what in your area.

## 4. When it trips
- Don't reset a trip until you know why it happened. Restart follows the procedure,
  with the field operator confirming valve positions locally.
- After a real ESD, restart is a major operation; after a spurious trip, report the
  faulty instrument and don't bypass it without authorisation (bypasses are logged
  and time-limited).

## 5. Emergencies and muster
- On the general alarm, go to your muster station (lifeboat or temporary refuge) by the
  designated route, carry your T-card/tag, and report. Be accounted for quickly.
- Know your secondary route and your role (fire team, first aid, lifeboat coxswain).

## 6. Logistics
Crane lifts and helicopter operations have their own controls (lift plans, banksmen,
helideck crew). Keep personnel out of the lift path; secure loose items before
helicopter arrival.

## Gotchas
- Handover is the most dangerous hour: permits and isolations open across shifts must be
  explicitly handed over face-to-face.
- An unlogged bypass on a safety-critical element is a major accident precursor.
- Small leaks matter: hydrocarbon releases are reported and investigated.

## Verify
- [ ] Permit covers the job, isolations proven, gas test current.
- [ ] SIMOPS conflicts checked.
- [ ] Trip cause understood before reset; bypasses logged.
- [ ] Muster route and role known.
- [ ] Handover covered open permits, isolations, bypasses and alarms.
