---
id: repair-maintenance.heavy-equipment-industrial-machinery-repair.millwrighting-machinery-installation.machine-base-levelling-grouting-and-laser-shaft-alignment
name: machine-base-levelling-grouting-and-laser-shaft-alignment
category: repair-maintenance
field: heavy-equipment-industrial-machinery-repair
product: millwrighting-machinery-installation
tags: [millwrighting-machinery-installation, millwright, machinery-installation, levelling, precision-level, machinist-level, datum, anchor-bolts, jacking-screws, epoxy-grout, cementitious-grout, baseplate, soleplate, soft-foot, shims, stainless-shims, laser-shaft-alignment, easy-laser, pruftechnik, fixturlaser, dial-indicator, rim-and-face, reverse-indicator, coupling-alignment, thermal-growth, pipe-strain, gearbox, conveyor-drive]
level: advanced
status: draft
description: "Set new industrial machinery: datum and levelling, anchor bolts and epoxy grouting, soft-foot correction, and laser shaft alignment to tolerance tables, including thermal growth."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting machinery: levelling, grouting and laser shaft alignment

**Goal:** install a driven machine (pump, fan, gearbox, conveyor drive) on a base that
stays flat and solid, then align the shafts so couplings, seals and bearings last.
For in-service pump and motor work (seals, bearings, VFD faults) see
`repair-maintenance.building-services-equipment-maintenance.pump-motor-maintenance.seal-bearing-alignment-and-vfd-fault-service`.

## 1. Datum and setting out
- Establish centrelines and an elevation datum from the drawings (a benchmark, not the
  floor). Mark centrelines on the foundation with scribed brass plugs or paint lines.
- Check the foundation: concrete cured (commonly 28 days for full strength), laitance
  chipped off to sound aggregate where grout will bond, anchor bolt positions and
  projection against the template.

## 2. Set and level the base
1. Set the baseplate or soleplates on jacking screws or levelling wedges, not on the
   anchor nuts alone.
2. Level with a precision machinist's level (0.02 mm/m per division class) on machined
   pads, both directions. A common target is 0.05 mm/m or better on mounting pads;
   follow the machine maker's figure. (Draft note: tolerance varies widely by machine
   class — API 686 is a commonly referenced practice for process pumps.)
3. Check pad co-planarity with a straight edge and feeler gauges or an optical/laser
   level. Twisted baseplates cause soft foot you cannot shim away later.
4. Snug anchor bolts, recheck level, then form and **grout**.

## 3. Grouting
- **Epoxy grout** for high dynamic loads (compressors, large pumps): high strength,
  chemical resistant, needs temperature control (typically 10–30 °C) and exact mix
  ratios. **Cementitious non-shrink grout** for lighter or static equipment.
- Pre-wet concrete for cementitious grout; keep it dry for epoxy. Pour from one side
  so air escapes; use a head box. Fill baseplate cavities fully — tap-test afterwards
  and drill/inject voids.
- Remove or back off jacking screws after cure so the grout carries the load, then
  torque anchors to spec.

## 4. Soft foot
- With the motor bolted down, loosen one foot at a time with a dial indicator on it.
  Movement over about 0.05 mm (0.002 in) is soft foot.
- Correct with clean, burr-free stainless precut shims, maximum 3–4 per foot (one thick
  rather than many thin). Find bent/angled feet with feeler gauges at each corner.
- Check **pipe strain** next: disconnect flanges with indicators on the shaft; movement
  over about 0.05 mm means pipe supports must be corrected, not the machine forced.

## 5. Laser shaft alignment
1. Lock out both machines. Mount laser heads (Easy-Laser, Prüftechnik, Fixturlaser) on
   the shafts with chain brackets close to the coupling.
2. Enter dimensions: head separation, coupling centre, front and rear foot positions.
3. Rotate both shafts together through at least 90° (more is better); the system
   reports vertical and horizontal **offset** and **angularity** plus foot corrections.
4. Correct vertical first with shims, then horizontal with jack bolts. Re-measure.
5. Typical tolerance for 1500 rpm: offset about 0.07 mm and angularity about
   0.07 mm/100 mm; tighter at 3000 rpm (around 0.04 mm and 0.05 mm/100 mm).
   (Draft note: use the coupling or machine maker's table where one exists.)
6. Enter **thermal growth** targets for hot equipment (steam turbines, hot pumps,
   gearboxes) so it aligns at running temperature.
Dial indicator rim-and-face or reverse-indicator methods work when no laser is
available; measure and correct bracket sag first.

## Gotchas
- Aligning before fixing soft foot — the readings change every time a bolt is tightened.
- Flexible couplings tolerate misalignment; bearings and seals do not.
- Torque foot bolts in the same sequence each time you measure.

## Verify
- [ ] Base level and pads co-planar to spec before grouting; grout void-free.
- [ ] Soft foot under 0.05 mm on every foot; no pipe strain.
- [ ] Final alignment within tolerance with bolts at final torque, report saved.
- [ ] Hot alignment check or thermal offsets applied where needed.
- [ ] Vibration baseline taken after start-up.
