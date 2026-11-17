---
id: manufacturing-production.cnc-machining-production.cnc-turning-production.bar-fed-turning-sub-spindle-transfer-and-unattended-running
name: bar-fed-turning-sub-spindle-transfer-and-unattended-running
category: manufacturing-production
field: cnc-machining-production
product: cnc-turning-production
tags: [cnc-turning-production, cnc-lathe, turning-centre, turning-center, bar-feeder, bar-feed, bar-stock, spindle-liner, bar-pull, part-catcher, parts-catcher, sub-spindle, counter-spindle, part-transfer, spindle-synchronisation, live-tooling, y-axis, c-axis, polar-interpolation, chip-control, chip-breaker, bird-nesting, lights-out, unattended-machining, tool-life-management, sister-tooling, high-pressure-coolant, end-of-bar, cnc-machining-production]
level: practitioner
status: draft
description: "Run bar-fed lathes on repeat work: bar feeder and liner setup, synchronised sub-spindle pickoff and cutoff, live tooling, chip control, and the safeguards that make lights-out turning safe."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bar-fed turning, sub-spindle transfer and unattended running

**Goal:** a turning centre that loads its own bar, finishes both ends of the part,
drops it safely and keeps going for a shift (or a night) without a crash, bird's
nest or a spindle full of scrap.

*Draft: generic practice; M-codes for bar feed, sub-spindle clamp/sync and parts
catcher are builder-specific — use the machine's own list.*

## 1. Bar feeder setup
- **Bar diameter vs spindle liner/channel:** liner bore typically 1–3 mm over bar size
  (vendor guidance varies). Too loose = whip and vibration at speed → rpm limits.
- **Straight bar, chamfered ends**; bent bars and burrs cause loading faults and runout.
- **Remnant length** set so the last part is fully supported in the collet/chuck;
  the bar feeder measures and ejects the remnant.
- **Bar push/pull method:** with a servo bar feeder, set face position with a stop
  (turret-mounted bar stop) or a programmed push length; check repeatability over a
  full bar.
- Set the max rpm for the bar size and liner — long unsupported bars whip violently.

## 2. Main spindle → sub-spindle transfer
1. Main spindle finishes op 1 features (face, OD, bore).
2. Sub-spindle moves to pickoff position; **spindles synchronised** (speed, and phase if
   live-tool features on both ends must align).
3. Sub-spindle collet/chuck closes on the part; confirm clamp (pressure switch).
4. **Cutoff** with the parting tool; a **cutoff confirmation** check (torque/position
   check or a probe touch) proves separation before the sub pulls away.
5. Sub-spindle withdraws; main spindle bar feed advances for the next part.
6. Op 2 on the sub-spindle (back face, chamfer, back-working), then eject into the
   **parts catcher/conveyor**.
- Pickoff grip length and pressure must not mark finished surfaces; use soft collets or
  lower pressure on thin walls.

## 3. Live tooling and Y-axis
- Cross-holes, flats, keyways with driven tools: C-axis indexed (spindle locked) or
  interpolated (polar/cylindrical interpolation, `G12.1`/`G07.1` on FANUC-type controls).
- Y-axis machines can mill off-centre without polar interpolation — better finish on flats.
- Driven tool holders have speed and torque limits well below the main spindle — check
  holder ratings.

## 4. Chip control (the lights-out killer)
- Long stringy chips wrap the part, the tool and the parts catcher. Select insert
  **chip breaker geometry** for the depth/feed actually used (finishing breakers need
  enough feed to work).
- Use **high-pressure coolant** through the tool to break chips in sticky materials.
- Interrupted feed (chip-breaking cycles, short dwells) in drilling and grooving.
- Check the chip conveyor capacity for a full night's volume.

## 5. Lights-out safeguards
- **Tool life management** with sister tools for wear items (inserts, drills).
- **Broken tool detection:** load monitoring or a tool-setter/probe check on small
  drills and taps.
- **Part presence and length check** (probe or bar stop touch) to catch short bars and
  failed cutoffs.
- **End-of-bar/end-of-material** stops safely, and machine alarms trigger a page/SMS.
- Thermal warm-up cycle before a long run; first parts after warm-up measured.
- **In-process gauging** on a sample basis with automatic wear-offset update where
  the control supports it.
- Fire risk: oil-based coolant + unattended = fire suppression and a risk assessment.

## Gotchas
- A part that fails to cut off gets dragged by the sub-spindle — crash. Always confirm.
- Parts catcher timing: extend too early and it gets hit by the turret.
- Bar feeder alarms often mean a bent bar or a dirty channel, not a fault in the feeder.

## Verify
- [ ] Liner correct for bar size; rpm limit set for unsupported length.
- [ ] Cutoff confirmation and clamp checks in the program.
- [ ] Chips break into manageable "6s and 9s" at the production feed.
- [ ] Sister tools and broken-tool checks active for every critical tool.
- [ ] A full bar run attended before going unattended.
