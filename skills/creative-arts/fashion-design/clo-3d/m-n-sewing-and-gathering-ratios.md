---
id: creative-arts.fashion-design.clo-3d.m-n-sewing-and-gathering-ratios
name: m-n-sewing-and-gathering-ratios
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-sewing, m-n-sewing, clo-gathering, clo-ruffles, clo-elastic-gathers]
level: practitioner
status: draft
description: "Use M:N segment and free sewing in CLO for one-to-many seams and gathers: connecting multiple edges, length ratios for ruffles and elastic, and checking results."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# M:N sewing and gathering ratios

**Goal:** sew several edges to several others in one operation and create controlled gathers
by sewing long edges to shorter ones.

## M:N Segment / M:N Free Sewing
1. Choose **M:N Segment Sewing** (or M:N Free Sewing).
2. Select the first group of segments (Shift/click to add multiple), press Enter.
3. Select the second group, press Enter. CLO distributes the sewing across the groups
   proportionally to their lengths.
4. Use for a skirt waist sewn to a bodice made of several panels, a waistband sewn to
   multiple pleated panels, or a ruffle sewn along several edges.

## Gathering by length difference
- Sew a long edge to a short one: the long edge is compressed into gathers.
- Ratio from real-world fullness (see the gathers draping skill): 1.5:1 to 3:1 depending on
  fabric weight.
- Reduce **particle distance** on the gathered piece (e.g. 5-10 mm) to resolve folds.
- Add an **elastic** property on a sewing or internal line to gather by elasticity (Elastic
  tool/property with ratio) for elastic waists and cuffs.

## Checking
- Simulate; inspect gather distribution. If gathers bunch at one end, split the sewing into
  matched sections (notch to notch) so distribution is controlled.
- Check that the shorter edge didn't stretch instead of the longer gathering: increase the
  shorter piece's stiffness or strengthen it temporarily.

## Gotchas
- Too much ratio with coarse mesh produces jagged spikes.
- M:N sewing across pieces in inconsistent directions twists; check pairing colours.
- Gathers on stiff fabric presets look unrealistic; set the real fabric first.

## Verify
- [ ] Ratio set from the real design fullness.
- [ ] Gathers distributed as intended (sectioned if needed).
- [ ] Particle distance fine enough on gathered pieces.
