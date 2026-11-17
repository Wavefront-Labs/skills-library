---
id: handcrafts.weaving.weave-drafting.reading-and-writing-weave-drafts
name: reading-and-writing-weave-drafts
category: handcrafts
field: weaving
product: weave-drafting
tags: [weave-drafting, weaving-draft, drawdown, threading, tie-up, treadling, liftplan, rising-shed, sinking-shed, jack-loom, counterbalance-loom, countermarch, twill, plain-weave, point-twill, overshot, colour-and-weave, profile-draft, wif-file, weaving-software, fiberworks, weavedesign, weaving]
level: practitioner
status: draft
description: "Read a weave draft (threading, tie-up, treadling, drawdown), draw down a twill by hand or software, and convert between rising-shed and sinking-shed looms."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading and writing weave drafts

**Goal:** look at a draft and know how to thread, tie up and treadle it — and predict the
cloth by drawing it down before you warp.

## The four parts of a draft
Drafts are drawn on squared paper. Conventions vary (North American vs European, top
vs bottom placement) so always check the legend.
1. **Threading** (usually top): rows = shafts, columns = warp ends. A mark in row 3,
   column 7 = end 7 goes on shaft 3. Read in the direction the draft shows (commonly
   right to left).
2. **Tie-up** (corner box): rows = shafts, columns = treadles. A mark = that shaft is
   tied to that treadle.
3. **Treadling** (side): rows = picks (weft passes), columns = treadles. A mark = press
   that treadle for that pick.
4. **Drawdown** (the big grid): the predicted interlacement; a filled square usually =
   warp on top.
A **liftplan** replaces tie-up + treadling for dobby and table looms: each pick row shows
which shafts lift directly.

## Drawing down by hand
For each pick (row) and each end (column):
1. Find which treadle is pressed for that pick.
2. From the tie-up, list the shafts tied to that treadle.
3. If the end's shaft (from threading) is in that list, fill the square (warp up on a
   rising-shed loom).
Do it for a full repeat. Then look: is it balanced? any long floats?

## Worked example: 2/2 straight twill on 4 shafts
- Threading: 1, 2, 3, 4 repeating.
- Tie-up (rising shed): T1 = shafts 1+2, T2 = 2+3, T3 = 3+4, T4 = 4+1.
- Treadling: 1, 2, 3, 4 repeating.
- Drawdown: a diagonal line moving one end per pick — twill. Each end passes over 2, under 2.
- Point twill: thread 1-2-3-4-3-2 and treadle 1-2-3-4-3-2 for diamonds.

## Rising vs sinking shed
- **Jack looms** (rising shed): tie-up marks = shafts that **rise**.
- **Counterbalance looms** (sinking shed, typically): tie-up marks may show shafts that
  **sink**. Countermarch looms tie both.
- Converting: a sinking-shed tie-up is the inverse of the rising one — swap marked and
  blank squares. The cloth is the same, just woven face-down (you see the back on the loom).
- Most published drafts say which convention they use; if not, check for a legend.

## Floats and practicality
- Count the longest float (warp or weft passing over many threads unbound). Floats longer
  than ~6 mm on clothing snag; for upholstery or rugs even shorter is better. Common rule of
  thumb, not a standard.
- Make sure every end is bound somewhere in the repeat, or it'll float the full cloth length.

## Colour-and-weave
- Add a colour order row above the threading and a weft colour column by the treadling.
  The same structure (e.g. plain weave) with alternating dark/light ends and picks gives
  log cabin; houndstooth comes from 4 dark/4 light in a 2/2 twill.

## Software
- Weaving programs (e.g. Fiberworks, WeaveDesign, iWeaveIt, free online drawdown tools)
  draw down instantly and read/write **WIF** (Weaving Information File), the standard
  exchange format. Check the program's rising/sinking setting before printing a plan.

## Gotchas
- Mismatched conventions are the top source of "the cloth looks nothing like the picture";
  confirm the direction of reading and shed type.
- A drawdown shows structure, not yarn behaviour: sett and fibre change the look; weave a sample.

## Verify
- [ ] You can name each draft part and the convention it uses.
- [ ] Hand drawdown of a repeat matches the published drawdown or software output.
- [ ] Longest float checked against the cloth's intended use.
- [ ] Tie-up converted correctly if your loom's shed differs from the draft's.
