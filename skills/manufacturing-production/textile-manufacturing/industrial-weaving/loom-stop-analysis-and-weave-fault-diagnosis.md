---
id: manufacturing-production.textile-manufacturing.industrial-weaving.loom-stop-analysis-and-weave-fault-diagnosis
name: loom-stop-analysis-and-weave-fault-diagnosis
category: manufacturing-production
field: textile-manufacturing
product: industrial-weaving
tags: [industrial-weaving, weaving-mill, loom, air-jet-loom, rapier-loom, projectile-loom, water-jet-loom, picanol, toyota, itema, dornier, warp-stop, weft-stop, loom-efficiency, warping, sizing, drawing-in, tying-in, warp-tension, shed, broken-end, broken-pick, starting-mark, stop-mark, reed-mark, float, double-pick, missing-end, weft-bar, fabric-inspection, four-point-system, greige]
level: practitioner
status: draft
description: "Raise loom efficiency and cut weave faults: read stop data by warp and weft, find the root cause in yarn, sizing, tension or settings, prevent starting marks, and classify faults at greige inspection."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loom stop analysis and weave fault diagnosis

**Goal:** fewer stops per loom and fewer fabric faults — two goals that are linked,
because every stop risks a **starting mark** and every repair risks a missing or
broken end. Weavers who just restart looms all shift fight the same faults forever.

## 1. Read the stop data
Modern looms (Picanol, Toyota, Itema, Dornier) log stops by cause. Report per loom,
per style, per shift:
- **Warp stops** per 10⁵ picks (or per hour) — broken warp ends.
- **Weft stops** — weft not arriving (air-jet), rapier transfer failures, weft breaks.
- Other: selvedge, leno, mechanical, electrical, doff.
Compare looms on the **same style**: one loom far worse than its neighbours = loom
setting; all looms bad on a beam/lot = yarn or preparation.

## 2. Warp stops — usual roots
- **Sizing** (size pick-up, abrasion resistance, hairiness laid down) — the most common
  root cause for cotton/blends; check size recipe, pick-up and stretch at the slasher.
- Weak places/neps in the yarn (spinning quality), knots/splices from winding.
- **Warp tension** too high or uneven; back-rest and let-off settings.
- **Shed geometry**: shed too large/early, heddles and dropwires worn, reed damage.
- Humidity in the weaving shed too low → more warp breaks (static, brittle size).
- **Drawing-in errors** (wrong heddle/dent) show up as faults from the first metre.

## 3. Weft stops — usual roots (air-jet)
- Main/relay nozzle pressure and timing for the yarn; weft yarn hairiness and count
  variation.
- Weft accumulator (feeder) tension and package quality (poorly wound cones).
- Profile reed condition, and shed not open enough when the pick flies.
- Rapier: gripper wear and transfer timing.

## 4. Starting marks
When the loom restarts after a stop, the fabric can show a thick or thin bar because
the cloth fell back or the warp relaxed. Prevent with the loom's **anti-starting-mark**
settings (pick finding, let-off/take-up compensation, slow start) tuned per style.
Long stops (break time, waiting for a repair) make bigger marks — respond to stops fast.

## 5. Common fabric faults and what they mean
| Fault | Cause |
|---|---|
| Missing end (warp-direction line) | End broken and not repaired / dropwire not stopping |
| Broken pick / missing pick | Weft fault, weft detector settings |
| **Double pick** | Weft feeler/detection, restart sequence |
| **Reed mark** (warp-direction streak) | Bent/damaged reed dents |
| Float | Ends not interlacing — heald/shed fault, broken heald, fluff |
| **Weft bar** (weft-direction band) | Weft lot/count mix, take-up fault, starting mark |
| Slubs/thick places | Yarn quality, fly woven in (cleaning) |
| Tight/slack ends | Beam winding tension at warping |

## 6. Inspection and grading
Greige fabric is inspected on frames under lighting; faults marked and graded, commonly
with the **4-point system** (points by fault length, limit per 100 sq yd/m²) unless the
customer specifies otherwise. Feed fault types back by loom and beam, daily.

## 7. Beam changes
Tying-in a new warp to the old (knotting machines) vs drawing-in from scratch for a
new style. Verify drawing-in plan, ends count and pattern before the loom runs a metre.

## Gotchas
- Restarting with a broken end tied in wrong position (crossed) creates a float the
  length of the beam until noticed.
- Fluff build-up (cleaning schedule, overhead blowers) causes both stops and slubs.
- Changes to loom speed improve output only if stops don't rise faster — check net efficiency.

## Verify
- [ ] Stops per 10⁵ picks reported per loom/style; outlier looms investigated.
- [ ] Root cause assigned (sizing, yarn, loom setting, environment) for top stop causes.
- [ ] Anti-starting-mark settings applied per style.
- [ ] Fault points per 100 m² within customer limit and fed back by loom.

*Draft: loom-brand stop codes and settings vary; 4-point system details depend on the
standard (e.g. ASTM D5430) the customer uses.*
