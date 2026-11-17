---
id: repair-maintenance.heavy-equipment-industrial-machinery-repair.preventive-maintenance-inspection.pm-service-intervals-and-walkaround-condition-inspection
name: pm-service-intervals-and-walkaround-condition-inspection
category: repair-maintenance
field: heavy-equipment-industrial-machinery-repair
product: preventive-maintenance-inspection
tags: [preventive-maintenance-inspection, preventive-maintenance, pm-service, pm-intervals, 250-hour-service, 500-hour-service, 1000-hour-service, 2000-hour-service, service-meter-hours, fluid-sampling, oil-sampling, sos-fluid-analysis, filter-cut-open, walkaround-inspection, structural-crack-inspection, pin-and-bushing-play, pre-delivery-inspection, pdi, telematics, fleet-maintenance, work-order, cmms, backlog, lockout-tagout, heavy-equipment]
level: practitioner
status: draft
description: "Run 250/500/1000/2000-hour PM services on heavy equipment: fluid sampling, filter cut-open, structural crack walkaround, and recording findings so failures are caught before downtime."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PM services and condition walkaround on heavy equipment

**Goal:** turn each scheduled service into an inspection that finds the next failure
early, not just an oil change — and record it so the fleet history is useful.
For lab interpretation of samples see
`repair-maintenance.reliability-engineering-failure-analysis.oil-analysis.oil-sampling-and-interpreting-lab-results`;
for choosing which tasks a PM should contain see
`repair-maintenance.reliability-engineering-failure-analysis.reliability-centred-maintenance.rcm-analysis-and-task-selection`.

## 1. Know the interval structure
Most heavy-equipment manuals stack services on service-meter hours, each including the
smaller ones. A typical pattern (Draft note: the OEM maintenance chart for the model
overrides this):
- **Daily / 10 h**: walkaround, fluid levels, grease high-load pins, air filter
  indicator, water separator, track or tyre condition.
- **250 h**: engine oil and filter (on many engines; some run 500 h), fuel water
  drain, belts, battery terminals, fluid samples.
- **500 h**: fuel filters, hydraulic return and pilot filters, breathers.
- **1000 h**: transmission and final drive oil on many machines, valve-lash check on
  some engines.
- **2000 h**: hydraulic oil (or by sample result), coolant test/change, swing drive,
  axle oils.
Shorten intervals for severe duty: dust, high load factor, extreme heat or cold, or
poor fuel.

## 2. Before you start
- Park level, lower all attachments to the ground, articulation lock fitted on
  articulated machines, wheels chocked.
- Lockout per site procedure. Relieve hydraulic tank pressure slowly; hot oil and
  coolant above 80 °C burn — open radiator caps only cool.
- Read the telematics/fault history and the operator's defect sheet first; they tell
  you where to look.

## 3. Fluid sampling — take samples right or not at all
- Sample at operating temperature, within about 30 minutes of shutdown, from the
  **live sampling valve** (not the drain plug) using a vacuum pump or probe with a new
  tube each time.
- Flush the valve with some oil into a waste container before filling the bottle.
- Sample **before** changing the oil. Label with machine serial, compartment, hours on
  machine and hours on oil, oil brand/grade, and whether oil was topped up.
- Same compartments every time: engine, hydraulics, transmission, final drives,
  differentials, coolant. Trends matter more than one result.

## 4. Filter cut-open
- Cut used oil filters open with a filter cutter (not a grinder) and inspect the pleats
  under a light and a magnet. Bright non-magnetic flakes (bearing material, bronze,
  aluminium) or magnetic glitter mean a failing component; sample again and plan.

## 5. Structural and component walkaround
Work the same route every time, with a light and a mirror, after a pressure wash where
possible:
- **Cracks**: boom and stick weld toes, bucket and loader linkage bosses, frame
  around the articulation hitch, counterweight mounts. Look for rust bleeding, paint
  cracks and fresh shiny metal lines.
- **Pins and bushings**: load and unload the attachment and watch for movement; note
  shims needed.
- **Hoses**: chafing, bulges, weeping fittings — mark leaks with a paint stick.
- **Undercarriage or tyres**: see
  `repair-maintenance.heavy-equipment-industrial-machinery-repair.undercarriage-track-service.undercarriage-wear-measurement-and-track-tensioning`.
- **Safety items**: seat belt, ROPS/FOPS damage, mirrors, cameras, horn, backup alarm,
  fire suppression system gauge, lights, steps and handholds.

## 6. Record and act
- Every finding goes into the work order or CMMS with machine hours and a photo,
  graded: safety (stop now), repair before next shift, schedule (backlog), monitor.
- Book backlog repairs with parts ordered so they fit into the next planned stop.
- After a new or rebuilt machine arrives, do a **pre-delivery inspection** (PDI): all
  levels, torques on critical fasteners, software versions, no codes, all safety
  items working, operator walked through the daily checks.

## Gotchas
- Samples from a drain plug or a cold machine give useless results.
- "Topped up" oil without recording the amount hides consumption problems.
- Skipping the walkaround because the job is "just a 250".

## Verify
- [ ] Machine grounded, locked out and pressure relieved before work.
- [ ] Every task on the OEM chart for this interval completed and signed.
- [ ] Samples taken hot, from valves, before draining, fully labelled.
- [ ] Filters cut open and findings noted.
- [ ] Defects graded and entered as backlog with hours and photos.
