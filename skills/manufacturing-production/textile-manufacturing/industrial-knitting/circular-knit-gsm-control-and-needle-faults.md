---
id: manufacturing-production.textile-manufacturing.industrial-knitting.circular-knit-gsm-control-and-needle-faults
name: circular-knit-gsm-control-and-needle-faults
category: manufacturing-production
field: textile-manufacturing
product: industrial-knitting
tags: [industrial-knitting, circular-knitting, weft-knitting, single-jersey, interlock, rib, fleece, mayer-and-cie, terrot, pailung, fukuhara, flat-knitting, stoll, shima-seiki, gauge, stitch-length, loop-length, yarn-input-tension, positive-feed, memminger, gsm, fabric-weight, barre, needle-line, broken-needle, latch, sinker, holes, dropped-stitch, spirality, lycra, elastane, oiling, fabric-inspection]
level: practitioner
status: draft
description: "Hold GSM and width on circular knitting machines by controlling stitch length, prevent barré from mixed yarn lots, and trace needle lines, holes and drop stitches to needle, sinker and feeder faults."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Circular knit GSM control and needle faults

**Goal:** greige fabric at the ordered **GSM** (grams per square metre) and width, free
of vertical needle lines, holes and barré. In circular knitting, the master variable is
**stitch (loop) length** — control that and GSM, width and shrinkage follow.

## 1. Stitch length is the setting that matters
- Fabric GSM depends on yarn count, stitch length and machine gauge. For a given yarn and
  machine, **longer stitch → lighter, more open fabric; shorter → heavier, tighter**.
- On **positive-feed** machines (tape-driven feeders, e.g. Memminger-type), the yarn
  delivery speed sets the course length: change the feed (pulley/servo setting), not the
  cam alone.
- Measure **course length** by marking a length of yarn on one feeder over a set number
  of needles, or run the **yarn length counter** (LFA). Divide by the needle count to get
  loop length; all feeders should agree — one feeder off makes a stripe.
- Lycra/elastane feeders: draft (stretch) setting changes both GSM and recovery.

## 2. GSM check
- Cut a sample with a GSM cutter (circular 100 cm² die), weigh on a balance, ×100 = GSM.
  Check greige against the greige target (not finished GSM — finishing changes it).
- Also check **width** (tube width) and wales/courses per cm.
- Adjust stitch length in small steps, run a length, re-test.

## 3. Barré — usually yarn, not machine
Horizontal bands repeating with the number of feeders:
- **Mixed yarn lots** (count or dye affinity differences) on the creel — the top
  cause. Keep one lot per machine; label cones.
- One feeder with different tension or loop length — check by feeder.
- Yarn package differences (winding tension, waxing).
Barré often only shows after dyeing, so prevention (lot control) matters more than
inspection.

## 4. Needle and sinker faults
| Fault | Likely cause |
|---|---|
| **Vertical needle line** (a wale looks different along the length) | Bent/worn needle, damaged latch, tight needle in trick, bent sinker |
| **Holes** | Yarn breaks/knots, latch closing early, high yarn tension, damaged needle hook |
| **Drop stitch / ladder** | Needle missing or broken, latch not opening |
| Oil stains/lines | Over-oiling, oil line leak, dirty needles |
| Lycra missing (shiny/stretchy loss) | Lycra break not detected; check stop motion |
- Replace needles **one at a time** with the correct type for the machine and gauge;
  replace sinkers adjacent if damaged. Many mills replace a full set at an interval.
- Keep **stop motions** (yarn break detectors, needle detector, fabric-fault camera
  if fitted) working — a disabled stop motion turns one broken needle into a roll of
  seconds.
- Fly/lint build-up: blow-out and cleaning schedule; fly woven in causes slubs and
  needle damage.

## 5. Spirality
In single jersey, the wales twist relative to courses (from yarn twist liveliness
and number of feeders). Control with yarn twist choice (lower twist/opposite twist
direction yarn), feeder count and finishing (compacting/setting). Check against the
customer's spirality limit after a wash test.

## 6. Flat knitting, briefly
Electronic flat machines (Stoll, Shima Seiki) run programmed patterns; GSM equivalent is
stitch value (cam setting) by section. Program revision and yarn carriers set-up checked
at changeover; first garment panel measured against the spec.

## Verify
- [ ] Loop length equal across feeders and at the target.
- [ ] Greige GSM, width and courses/wales on target.
- [ ] One yarn lot per machine; cones labelled.
- [ ] Stop motions active; needle faults repaired before continuing.
- [ ] Spirality checked after wash test where specified.

*Draft: target GSM relationships are machine- and yarn-specific; values not given.*
