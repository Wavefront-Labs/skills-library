---
id: architecture-construction.surveying-geomatics.total-station.setup-backsight-and-stakeout
name: setup-backsight-and-stakeout
category: architecture-construction
field: surveying-geomatics
product: total-station
tags: [total-station, surveying, setup, centring, levelling, tribrach, optical-plummet, laser-plummet, backsight, orientation, check-shot, resection, free-station, stakeout, setting-out, face-left, face-right, prism-constant, atr, robotic-total-station, leica, trimble, topcon, sokkia, geomatics]
level: practitioner
status: draft
description: "Total station workflow: set up over a mark, orient on a backsight, prove it with a check shot, then stake out and observe with the checks that catch blunders before they reach site."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Total station — setup, backsight and stakeout

**Goal:** get the instrument onto the right coordinates and bearing, prove it, and
then measure or set out points you can defend. Almost every total-station blunder is a
setup or orientation blunder, not a measurement one.

## 1. Setup over a known mark
1. Tripod roughly over the mark, head roughly level, legs pushed firmly in (on tarmac,
   use a tripod star or chain so legs can't creep in the sun).
2. Mount the instrument, centre with the laser or optical plummet using the footscrews.
3. Level the circular bubble with the **tripod legs** (extend/shorten), not footscrews.
4. Fine-level with footscrews against the electronic bubble/tilt display.
5. Re-check centring; slide the instrument on the tripod head to correct, re-level.
   Repeat until centred and level at the same time.
6. Measure **instrument height (HI)** to the trunnion mark, and the **target height (HT)**
   of the prism pole. Enter both. A wrong HI is a silent error in every level you shoot.

Free station / resection is the alternative when no mark is convenient: observe to
three or more known points (two is the minimum but gives no redundancy) and accept only
if the residuals are within your job tolerance.

## 2. Orientation (backsight)
- Set station coordinates, then sight the backsight point and let the software compute
  the bearing — or enter the bearing manually if working on an assumed grid.
- Observe a **distance** to the backsight as well as the angle; compare with the
  coordinate-derived distance. This catches the wrong mark, wrong coordinate and wrong
  prism constant in one go.
- **Check shot:** measure a third known point and compare coordinates and height.
  Typical site tolerance is around ±5–10 mm horizontal; your spec decides — note it.
- Re-observe the backsight at the end of the setup (and periodically during long
  setups). If the bearing has moved, the tripod settled or got knocked.

## 3. Prism constants and targets
Prism constants differ between makes (commonly 0 mm or −30 mm; mini prisms often
+17.5 mm on some systems). The constant in the instrument must match the prism on the
pole — mixing brands gives a constant distance error that a check shot to a nearby
point may not reveal. Use reflectorless only on surfaces you trust; edges and
glancing angles give the wrong distance.

## 4. Observing and face left / face right
For control and anything structural, observe on **both faces** (FL/FR) and take the
mean — it removes collimation and trunnion-axis errors. For detail pickup one face is
usually accepted. Run the instrument's collimation and compensator checks on a
calibration schedule and after any knock.

## 5. Stakeout
1. Load design points with a clear naming convention (gridline, offset, reference).
2. Stake from the setup that gives the shortest sight and a good angle to the target.
3. Give the pole holder "in/out, left/right" instructions from the instrument view, or
   let robotic tracking (ATR/lock) guide from the pole.
4. Mark, then **re-measure the mark you set** and record as-staked coordinates and the
   delta. Never trust the screen value at the moment you hammered the nail.
5. Set **offsets** (e.g. 1 m off the corner, outside the excavation) for anything that
   will be dug out or built over.

## Gotchas
- Heat shimmer over asphalt and long sights degrade fine pointing; work early or shorten sights.
- Enter temperature and pressure (ppm correction) — on long distances it matters.
- Scale factor: if design coordinates are on a projected grid and you measure ground
  distances, check whether the job uses a combined scale factor. Ask, don't assume (see
  control-networks skill).
- A prism pole bubble out of adjustment puts every shot off by the tilt × pole height.

## Verify
- [ ] HI and HT recorded and entered; prism constant matches the prism in use.
- [ ] Backsight distance agrees with coordinates; check shot within tolerance and logged.
- [ ] Backsight re-observed at end of setup with no significant change.
- [ ] Every staked point re-measured; as-staked deltas recorded.
- [ ] Offsets set for points that will be excavated.

*Uncertainty:* tolerances and prism constants above are typical values, not
manufacturer-specific; confirm against your instrument manual and project spec.
