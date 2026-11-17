---
id: handcrafts.metalsmithing-manual-welding.sheet-metal-fabrication.laying-out-and-folding-a-sheet-metal-box
name: laying-out-and-folding-a-sheet-metal-box
category: handcrafts
field: metalsmithing-manual-welding
product: sheet-metal-fabrication
tags: [sheet-metal-fabrication, sheet-metal, sheetmetal, box-and-pan-brake, finger-brake, folder, press-brake, bend-allowance, bend-deduction, k-factor, inside-radius, flat-pattern, layout, relief-cuts, corner-relief, mild-steel-sheet, galvanised-steel, galvanized, aluminium-sheet, aluminum, 5052, 3003, hand-shears, aviation-snips, throatless-shear, guillotine, hemmed-edge, flange, tray, enclosure, guard, duct]
level: practitioner
status: draft
description: "Lay out a flanged box or tray from flat sheet with correct bend allowance and corner reliefs, cut it, and fold it on a box-and-pan brake in the right order so every flange fits."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Laying out and folding a sheet-metal box

**Goal:** a one-off open box, tray or guard from a single flat blank whose outside
dimensions come out within about ±0.5 mm, with clean corners and no fold that
blocks the next.

## 1. Choose material and bend radius
- **Mild steel / galvanised:** 0.8–1.5 mm folds well; inside radius about 1× thickness.
- **Aluminium:** 5052-H32 and 3003-H14 fold cold at ~1–1.5× thickness radius.
  **6061-T6 cracks** on tight bends — avoid it or allow 3× thickness or more and
  bend across the grain.
- Note the rolling direction; bends **across** the grain crack less.

## 2. Calculate the flat pattern
Bending stretches the outside and compresses the inside; the neutral axis lies at
a fraction *K* of the thickness *T* from the inside.
- **Bend allowance (BA)** for a 90° bend = (π/2) × (R + K×T), where *R* = inside radius.
- K ≈ 0.33 for a tight air-bent radius (R ≤ T), rising to ~0.4–0.5 for larger radii
  (typical published range; your brake and material set the real figure).
- Simpler shop method — **bend deduction**: make a test bend in a strip of the same
  sheet, measure both outside legs, and BD = (leg1 + leg2) − strip length. For each
  90° fold, subtract BD from the sum of outside dimensions.
- Worked example: 1.0 mm mild steel, BD measured at 1.7 mm. A tray 200 × 150 outside
  with 30 mm flanges: blank = (30 + 200 + 30) − 2×1.7 = 256.6 mm by
  (30 + 150 + 30) − 3.4 = 206.6 mm.

## 3. Lay out
- Work from one machined or sheared datum edge. Scribe with a sharp scriber and
  steel rule; use an engineer's square off the datum.
- Mark **bend lines** (outside mould lines minus half the BD is accurate enough for
  craft work; or mark where the brake's clamp edge should sit — test first).
- **Corner relief:** cut out each corner square or with a drilled relief hole of
  diameter ≈ 2× thickness + radius at the intersection of bend lines, so the sheet
  does not tear when folded. For a closed corner add a 10–15 mm tab on two flanges
  to rivet or spot-weld.

## 4. Cut
- Shear long straight edges on a guillotine or bench shear; finish inside corners with
  aviation snips (red = left, green = right, yellow = straight, on the usual US
  colour convention).
- Deburr every edge with a file or deburring tool before bending — burrs crack bends
  and cut hands.

## 5. Fold — sequence matters
1. **Hems first** (if any): fold 180° in two steps, then flatten.
2. **Short sides next**, on the box-and-pan brake with full clamp width.
3. **Long sides last**, using **removable fingers** spaced to clear the already-
   formed short flanges.
- Align the bend line exactly with the clamping-bar edge; clamp; lift the apron in one
  steady pull. Springback: overbend 2–4° for mild steel, more for aluminium; check
  with a square and correct.
- Mallet over the tabs and fasten (pop rivets 3.2–4 mm at 25–40 mm pitch, spot or tack welds).

## Faults
- **Box oversize:** BD not deducted, or bend line set on the wrong side of the clamp.
- **Corner tears or bulges:** relief too small.
- **Flange clash:** wrong fold order or fingers not spaced.
- **Cracks along bend:** radius too tight for the temper, or bending along the grain.

## Safety
Sheet edges and swarf cut — gloves when handling, off when operating rotating
machines. Keep fingers clear of the brake clamp and shear blade. Galvanised sheet:
never weld or heat without fume extraction (zinc fume fever).

## Verify
- [ ] Bend deduction measured on a test strip of the same sheet and brake.
- [ ] Corner reliefs cut; all edges deburred before folding.
- [ ] Fold sequence planned so no flange blocks a later one.
- [ ] Each fold square (90° checked) after springback correction.
- [ ] Outside dimensions within tolerance; corners closed and fastened.
