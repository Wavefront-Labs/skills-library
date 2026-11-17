---
id: manufacturing-production.metal-plastics-fabrication-production.injection-moulding.moulding-defect-diagnosis-at-the-press
name: moulding-defect-diagnosis-at-the-press
category: manufacturing-production
field: metal-plastics-fabrication-production
product: injection-moulding
tags: [injection-moulding, injection-molding, plastics, moulding-defects, short-shot, flash, sink-marks, voids, warpage, warp, splay, silver-streaks, burn-marks, dieseling, jetting, weld-lines, knit-lines, flow-lines, drying, resin-dryer, dew-point, regrind, process-sheet, setter, mould-temperature, hold-pressure, cushion, engel, arburg, krauss-maffei, haitian, sumitomo-demag]
level: practitioner
status: draft
description: "Diagnose short shots, flash, sinks, warp, splay and burns at the moulding press: check what changed, read cushion and fill time, then fix material, machine, mould or process in that order."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Moulding defect diagnosis at the press

**Goal:** when a running job starts making bad parts, find the *cause* — not crank
the nearest knob. Most "process" problems on an established job are really a material,
machine or mould change; the validated process sheet was fine yesterday.

## 1. First: what changed?
Before touching a setting, compare against the **approved process sheet** and ask:
- New **material lot**, colour masterbatch or regrind ratio? Dryer refilled?
- Machine alarm, heater band out, check ring/non-return valve wear (cushion drifting)?
- Mould: water line disconnected or swapped, vent blocked, cavity damaged, hot-runner
  zone off?
- Shift change with someone "adjusting" settings? Check the machine's change log.
- Ambient: a cold morning shifts mould-temperature-controller behaviour on some jobs.

## 2. Read the machine's own numbers
On every shot, the controller (Engel, Arburg, KraussMaffei etc.) records:
- **Fill (injection) time** — rising fill time at the same velocity setting = viscosity
  up (wet/cold material, lot change) or a restriction.
- **Peak injection pressure** — at the pressure limit means the machine is
  pressure-limited and not actually following the velocity profile.
- **Cushion** — material left in front of the screw after hold. Zero cushion = the
  screw bottomed out, hold pressure isn't packing anything. Erratic cushion = leaking
  check ring.
- **Recovery (screw) time** — erratic = feed problems, bridging in throat, wet material.
Compare these with the values recorded at process approval.

## 3. Defect → first suspects
| Defect | Check first |
|---|---|
| **Short shot** | Shot size/transfer position, cushion zero, blocked nozzle or hot-runner tip, frozen gate, vents blocked, pressure-limited |
| **Flash** | Clamp tonnage/parting line damage or debris, too-high hold/transfer late, melt too hot, worn mould |
| **Sink / voids** | Hold pressure/time too low, gate freezing early, thick sections, cushion zero, mould too hot locally |
| **Warp** | Uneven mould temperature (check water circuits!), too-short cooling, ejection on hot part, packing differences |
| **Splay / silver streaks** | Wet material (dryer dew point, residence time), degraded material, excessive back pressure/screw speed |
| **Burn marks / dieseling** | Trapped air at end of fill — blocked vents, injection too fast at end |
| **Jetting** | Fast first-stage velocity through small gate; profile slower at gate |
| **Weld/knit lines** | Melt/mould too cold, vents at the weld location, gate location (design) |
| **Black specks** | Degraded material in hot-runner/barrel dead spots, contaminated regrind |

## 4. Material drying
Hygroscopic resins (PA, PC, PET, PBT, ABS to a lesser degree) must be dried to the
supplier's moisture spec. Check the **dryer dew point** (often −40 °C or lower on
desiccant dryers — confirm the supplier figure), drying temperature, and that the
hopper residence time is long enough for the current throughput. Over-drying some
grades (e.g. PA) causes yellowing.

## 5. Fixing it
- Change one thing, run 10–20 shots to stabilise, inspect, record.
- If you must move outside the process sheet's window, that is a **deviation** — get
  approval, and quarantine parts made while hunting.
- Put back anything that turned out not to matter.
- After the fix, confirm critical dimensions (CTQs) per the control plan, not just
  appearance.

## Gotchas
- Raising pressure to fix shorts can cause flash and stuck parts — fix the cause.
- A swapped water line (in/out reversed, or circuits crossed) produces warp and sink
  that looks exactly like a process problem.
- Purging with the nozzle against the mould or without a guard is a burn hazard; purge
  into the purge guard per safety procedure.

## Verify
- [ ] Settings match the approved process sheet, or a deviation is approved.
- [ ] Cushion stable and non-zero; fill time and peak pressure back at reference.
- [ ] Material dryer dew point and residence time confirmed.
- [ ] CTQ dimensions checked after the fix; suspect parts quarantined.

*Draft: dew-point and drying numbers vary by resin grade — always use the material
datasheet.*
