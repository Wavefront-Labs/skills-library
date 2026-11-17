---
id: repair-maintenance.building-services-equipment-maintenance.elevator-escalator-maintenance.lift-door-and-safety-routine-maintenance
name: lift-door-and-safety-routine-maintenance
category: repair-maintenance
field: building-services-equipment-maintenance
product: elevator-escalator-maintenance
tags: [building-services-equipment-maintenance, elevator-escalator-maintenance, elevator, lift, escalator, lift-maintenance, door-operator, landing-doors, door-locks, door-interlocks, light-curtain, door-restrictor, overspeed-governor, safety-gear, brake-inspection, traction-lift, hydraulic-lift, ropes, callback, fault-log, loler, asme-a17-1, en-81, lift-pit, top-of-car, escalator-comb-plate, step-chain, entrapment]
level: practitioner
status: docs-checked
description: "Routine lift and escalator maintenance for competent technicians: safe car-top and pit access, door operator and lock checks, brake and governor inspection, callback diagnosis."
sources: ["https://www.hse.gov.uk/work-equipment-machinery/passenger-lifts.htm", "https://www.hse.gov.uk/work-equipment-machinery/thorough-examinations-lifting-equipment.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lift door and safety routine maintenance

**Goal:** a planned routine that keeps doors (the source of most callbacks and many
injuries) reliable and proves the safety chain works. **Lift work is restricted to
trained, authorised lift technicians** working to the maker's procedures and local law
(e.g. ASME A17.1/CSA B44 in North America, EN 81 / BS 7255 and LOLER thorough
examinations in the UK, at least every six months for lifts carrying people at work). This skill is an orientation and checklist, not a licence.

## 1. Safe access — every visit
1. Put the lift on **inspection/maintenance control**; display "out of service" at every
   landing.
2. **Entering car top:** call the car below the landing, open the landing door with the
   unlocking key, press the car-top **stop switch before stepping on**, switch to
   inspection, test that the car won't run on normal calls and that the stop works.
3. **Pit:** stop switch at pit entry first, check buffer and car position, never be in the
   pit with the car on normal service.
4. Never wedge landing doors open unattended; a barrier is needed for open shafts.
5. Two-person working where the risk assessment/maker requires it.

## 2. Door system (most callbacks)
- **Door operator:** check speed profile — smooth opening, slowing near the end, no
  slamming; closing force/kinetic energy within the code limit (confirm in the standard for the
  jurisdiction).
- **Light curtain / safety edge:** test by breaking beams at several heights; doors must
  reopen without contact.
- **Landing door locks and contacts:** check engagement depth of the lock hook (minimum
  engagement before the contact makes, per the standard), clean contacts, check
  that the car cannot run with any landing door open.
- **Sills and tracks:** vacuum debris from sill grooves; foreign objects in the sill are a
  top cause of door faults.
- **Door rollers, hangers, closers:** wear, eccentric roller adjustment, landing door
  self-closing weight/spring works when released.

## 3. Machine room / machinery space
- **Brake:** inspect linings, plunger stroke, air gap to maker spec; check it holds the test load
  per the periodic test regime. Look for oil on linings.
- **Overspeed governor:** rope condition, free rotation, electrical overspeed switch; full
  trip test at periodic examinations by authorised persons.
- **Ropes:** diameter reduction, broken wires, rouge (internal corrosion), tension
  equalisation.
- **Hydraulic lifts:** oil level and temperature, leaks at the jack and valve, re-levelling
  frequency (creeping indicates a leak or valve problem).
- **Controller fault log:** read and clear only after recording; recurring codes guide
  the next visit.

## 4. Escalators (brief)
Check comb plates for broken teeth, step/skirt gap (tight limits per the standard), handrail speed matches steps, stop buttons and safety switches (comb, skirt,
handrail inlet, missing step) operate. Clean step track debris.

## 5. Callback diagnosis
1. Read the controller fault log and time stamp before resetting.
2. Ask what passengers saw (stopped between floors, doors reopening, levelling step).
3. Doors reopening repeatedly → light curtain alignment/dirty sill; stopped with doors
   shut → safety chain opened (find which contact: use the controller's chain diagnostics).
4. Fix, test with several runs on normal service, log the root cause.

## Entrapments
Follow the site rescue procedure — release by trained persons only; communicate with
passengers via the alarm intercom; never attempt manual hand-winding without training.

## Gotchas
- Bridging a door contact "temporarily" has killed people. Never leave a bridge in.
- A shared building's facilities team must not adjust lifts themselves — call the contractor.

## Verify
- [ ] Inspection mode and stop switches tested before every access.
- [ ] All landing doors lock and the car won't move with one open.
- [ ] Door reopening devices tested at several heights.
- [ ] Brake, governor, ropes inspected and recorded.
- [ ] Fault log recorded; lift returned to service after test runs; logbook signed.

## Checked

Date checked: 2026-10-25. Jurisdiction: United Kingdom (LOLER) and North America (ASME A17.1/CSA B44) by name; the standard in force governs.
HSE passenger lifts and thorough examination pages: passenger lifts at work are subject to LOLER and PUWER, lifts carrying people must be thoroughly examined by a competent person at least every six months (goods-only lifts every 12 months unless a written scheme says otherwise). EN 81, ASME A17.1 and BS 7255 are paywalled, so numeric limits taken from them (door closing force and kinetic energy, lock engagement depth, brake test load, escalator gap) were removed and replaced by 'per the standard'.

Method: documentation only; no commands were run.
