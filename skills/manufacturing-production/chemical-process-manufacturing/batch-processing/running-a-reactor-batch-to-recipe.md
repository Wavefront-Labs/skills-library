---
id: manufacturing-production.chemical-process-manufacturing.batch-processing.running-a-reactor-batch-to-recipe
name: running-a-reactor-batch-to-recipe
category: manufacturing-production
field: chemical-process-manufacturing
product: batch-processing
tags: [batch-processing, batch-reactor, isa-88, s88, recipe, master-recipe, control-recipe, unit-procedure, operation, phase, charging, reactor-charging, exotherm, dosing, semi-batch, in-process-control, ipc, sampling, batch-record, ebr, batch-consistency, golden-batch, endpoint, jacket-temperature, cycle-time, chemical-plant, specialty-chemicals]
level: practitioner
status: draft
description: "Execute a chemical batch to its recipe: pre-batch checks, charging and dosing, controlling an exotherm, taking in-process samples, hitting the endpoint and keeping batch-to-batch consistency."
sources: ["ANSI/ISA-88 batch control models (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a reactor batch to recipe

**Goal:** produce a batch that matches the master recipe and the last good batch —
same charges, same profile, same endpoint — with every deviation caught and recorded.

## 1. Think in ISA-88 terms
- **Master recipe** — the approved procedure for a product. **Control recipe** — the
  copy executing for this batch, with this batch's quantities.
- **Procedure → unit procedure → operation → phase** (e.g. *Charge solvent*, *Heat to
  60 °C*, *Dose monomer over 3 h*, *Hold*, *Sample*, *Cool*, *Transfer*).
- Whether phases run automatically (DeltaV Batch, Experion Batch, Rockwell
  FactoryTalk Batch) or from a paper batch sheet, the discipline is the same: do the
  phase, confirm its end condition, record, move on.

## 2. Pre-batch checks (the batch is mostly won here)
- Vessel clean, dry and released (cleaning record, previous product compatible).
  Residual water in a vessel for a water-sensitive chemistry is a classic upset.
- Valves lined up per the line-up sheet; bottom valve closed; vent and scrubber or
  condenser in service; agitator and jacket service available.
- Raw materials: right material, right lot, released by QC, quantity staged and labelled.
- Instruments: load cells zeroed or tared, temperature probes reading sensibly vs a
  second measurement, pH/conductivity probes calibrated if used.

## 3. Charging and dosing
- Charge in **recipe order** — order matters for heat of mixing, solubility and
  safety (e.g. acid into water, never the reverse).
- Verify every charge two ways where you can: load cell or flowmeter total **and**
  the drum/IBC weight or tank level change. Record actual against target.
- **Semi-batch dosing of a reactive component:** the dose rate is the heat-control
  knob. Confirm the reaction is consuming feed (exotherm visible as jacket
  outlet–inlet ΔT or as cooling demand) before increasing rate. If temperature does not
  respond after the first few percent, **stop dosing** — unreacted accumulation of
  reactant followed by sudden initiation is a well-known runaway mechanism.
- Agitation must be confirmed running (motor current, not just the run signal) before
  dosing; a stopped agitator lets reactants layer.

## 4. Watching the reaction
Trend: reactor temperature, jacket in/out, dose total, pressure, agitator amps.
- Exotherm profile should overlay the "golden batch" profile. A late or missing
  exotherm, or one much sharper than usual, is a deviation — hold and call the
  chemist or supervisor.
- Rising pressure with stable temperature suggests gas evolution or a blocked vent.
- Agitator amps rising can indicate viscosity build — sometimes the endpoint signal,
  sometimes a gel forming.

## 5. In-process samples (IPC)
- Sample at the recipe points from a flushed sample point (discard the dead leg first).
- Label with batch, step, time. Hold the step until the result is in, unless the
  recipe explicitly says to continue.
- If the result is out of range, follow the **adjustment** in the recipe (extra
  hold time, a correcting charge calculated from the result). Never invent an
  adjustment; record and escalate.

## 6. Endpoint, discharge, record
- Endpoint is a measured condition (conversion, acid value, viscosity), not "the
  time is up".
- Before transfer: destination line-up checked, destination has room, filter in place.
- Complete the batch record as you go, not at end of shift: actual quantities, times,
  temperatures, deviations, signatures.

## Batch-to-batch consistency
Compare each batch to the last good ones: total cycle time, peak temperature, dose
duration, IPC values, yield. Drift in one of these across batches (e.g. longer dose
time each batch) points to fouling of the jacket, raw material lot change or
instrument drift before it becomes a reject.

## Verify
- [ ] Vessel release, line-up and raw-material lot checks signed before the first charge.
- [ ] Every charge recorded as actual vs target with a second confirmation.
- [ ] Reaction response confirmed before dose rate was increased.
- [ ] IPC results within range or adjustment done per recipe and recorded.
- [ ] Batch overlays the reference profile; deviations raised, not just noted.

*Draft note:* generic practice; specific limits (dose rates, hold criteria) come from
the product's process safety data and approved recipe.
