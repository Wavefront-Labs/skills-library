---
id: manufacturing-production.textile-manufacturing.garment-line-sewing.smv-paced-operation-and-seam-quality
name: smv-paced-operation-and-seam-quality
category: manufacturing-production
field: textile-manufacturing
product: garment-line-sewing
tags: [garment-line-sewing, sewing-line, apparel, garment-manufacturing, industrial-sewing-machine, lockstitch, stitch-301, overlock, serger, stitch-504, stitch-514, coverstitch, stitch-406, juki, brother, pegasus, yamato, smv, sam, standard-minute-value, operation-breakdown, line-balancing, bottleneck, efficiency, spi, stitches-per-inch, thread-tension, needle-size, skipped-stitches, seam-puckering, needle-damage, inline-inspection, traffic-light-inspection, aql, bundle-system]
level: practitioner
status: draft
description: "Run a paced garment sewing line: SMV and operator efficiency, balancing around the bottleneck, machine setup for seam quality (SPI, tension, needles), and fixing puckering and skips."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMV-paced operation and seam quality

**Goal:** a sewing line that hits its hourly target **and** makes seams that pass
inspection — because rework at end-of-line erases the efficiency you gained.

## 1. SMV and efficiency
- Each garment is broken into **operations** (e.g. "join shoulder – overlock",
  "attach collar – lockstitch") with a **SMV/SAM** (standard minute value): the time a
  trained operator needs at standard pace, including allowances. Usually from a
  time-study or predetermined system (e.g. GSD).
- **Operator efficiency** = (pieces × SMV) ÷ minutes worked × 100.
- **Line target per hour** = (operators × 60 × planned efficiency) ÷ garment SMV.
- Efficiency differences between operators are real: allocate high-skill operations
  (collars, plackets, visible topstitching) to skilled operators.

## 2. Line balancing
- Calculate each operation's required operators: (operation SMV ÷ takt time).
  Takt = available minutes ÷ target pieces.
- The **bottleneck** (slowest station) sets the line output. Balance by splitting an
  operation, adding a helper/second machine, or moving a skilled operator there.
- Watch **WIP** between stations: growing piles = downstream bottleneck; empty = upstream
  starving. Keep a small, steady buffer (bundle system or single-piece flow).
- Re-balance after the learning curve on a new style (efficiency rises over days).

## 3. Machine classes (know which does what)
- **Lockstitch (ISO 301)**: single needle, main seams, topstitching — strong, low stretch.
- **Overlock / serger (504, 514, safety stitch 516)**: edge finishing and seaming on
  knits; stretch.
- **Coverstitch / flatlock (406, 602, 605, 607)**: hems and flat seams on knits.
- **Chainstitch (401)**, **bartack**, **buttonhole**, **button sew** for specific ops.
Using a lockstitch on a stretch seam → seam cracks when the garment is stretched.

## 4. Setting up for seam quality
- **SPI** (stitches per inch) or SPCM per the tech pack — too few: weak, gaping seams;
  too many: puckering and fabric damage.
- **Needle**: size and point type for the fabric — ball point for knits (prevents
  needle cuts/holes), sharp for wovens; replace on schedule and immediately after a hit.
  Broken needle fragments are a **safety issue**: follow the broken-needle policy
  (find all pieces, log, possibly metal-detect garments).
- **Thread**: correct ticket/size and type (core-spun poly, textured for overlock
  loopers). Thread tension balanced: lockstitch interlock in the middle of the plies.
- **Feed**: differential feed on overlock to avoid waviness (stretched) or puckering
  (gathered) on knits; presser foot pressure light enough for fine fabrics.
- Sew a test seam on actual fabric before running bundles after any machine change.

## 5. Defect → first suspects
| Defect | Check |
|---|---|
| Skipped stitches | Needle bent/wrong size, needle–hook timing, thread path |
| Seam puckering | Tension too high, SPI too high, feed mismatch, thread shrinkage |
| Broken stitches | Wrong stitch type for stretch, thread too weak, tension |
| Needle holes / cuts in knits | Blunt or wrong needle point, too big needle |
| Wavy seams | Differential feed, operator stretching fabric |
| Open seam / raw edge | Seam allowance, overlock knife setting, operator guide |

## 6. In-line quality
- **Inline (roving) inspection** — e.g. traffic-light system: QC checks a sample from
  each operator per round; red = stop and fix before continuing.
- End-of-line 100 % inspection and **AQL**-based final audit per the buyer.
- Feed defects back to the operator immediately; root-cause recurrent ones to
  machine settings or training.

## Verify
- [ ] Line target derived from SMV and planned efficiency; bottleneck identified.
- [ ] Machines set to tech-pack SPI, correct needle and thread; test seam OK.
- [ ] Broken needles logged per policy.
- [ ] Inline inspection rounds done; red flags closed.
- [ ] End-of-line defect % and AQL results trended per line.

*Draft: SMV methods (GSD, MTM) and inspection systems differ between factories and
buyers.*
