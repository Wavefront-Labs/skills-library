---
id: manufacturing-production.textile-manufacturing.cutting-room-operations.marker-efficiency-spreading-and-cut-accuracy
name: marker-efficiency-spreading-and-cut-accuracy
category: manufacturing-production
field: textile-manufacturing
product: cutting-room-operations
tags: [cutting-room-operations, cutting-room, garment-manufacturing, apparel, marker-making, marker-efficiency, nesting, gerber, accumark, lectra, optitex, grain-line, nap, one-way, spreading, spreading-machine, ply-height, lay, end-loss, splicing, relaxation, shrinkage, auto-cutter, gerber-paragon, lectra-vector, straight-knife, notches, drill-holes, bundling, ticketing, shade-sorting, numbering, cut-order-plan, fabric-utilisation]
level: practitioner
status: draft
description: "Run a cutting room for yield and accuracy: marker efficiency and grain rules, relaxed and shade-controlled spreading, auto-cutter settings, notch accuracy and bundle ticketing for the sewing line."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Marker efficiency, spreading and cut accuracy

**Goal:** cut panels that are the right size, on grain, shade-consistent within each
garment — from as little fabric as possible. Fabric is typically the largest single cost
of a garment, so the cutting room is where most of the cost is won or lost.

## 1. Cut order plan and markers
- **Cut order plan**: group sizes and quantities into lays (e.g. which size ratio per
  marker, how many plies) to minimise markers, plies and leftover.
- **Marker making** in CAD (Gerber AccuMark, Lectra Diamino/Modaris, Optitex): nest all
  pattern pieces for the size ratio. **Marker efficiency** = pattern area ÷ marker area;
  compare against the target for that garment/fabric (knits, plaids and one-way
  fabrics are lower).
- Rules the marker must respect:
  - **Grain line** of every piece parallel to the warp (or as the pattern says);
    tilt allowance per the customer spec.
  - **Nap/one-way** fabrics (velvet, corduroy, prints with direction): all pieces
    the same way.
  - **Stripes/checks**: matching points — needs extra allowance or block cutting.
  - Width: marker width = **usable** fabric width (measure the actual rolls, minus
    selvedge); a marker wider than the narrowest roll makes cut-off panels.
- Mixed-size markers help efficiency but make shade control harder (below).

## 2. Fabric preparation
- **Relaxation**: knits and stretch fabrics shrink after unrolling — relax for the
  specified time (often 12–24 h for knits, confirm) before spreading, or cut panels
  come out small.
- **Shrinkage test** results (from fabric inspection) must match the pattern's built-in
  allowance; a different shrinkage lot needs a different pattern/marker.
- **Shade sorting**: rolls grouped by shade (shade bands/continuity cards). Never mix
  shades within a lay without numbering.

## 3. Spreading
- Spread by hand or machine (spreading machine with tension control). Plies
  **tension-free** (stretched plies shrink back after cutting), aligned to one edge,
  no folds or bows.
- **Ply height** within the cutter's limit (compressed height for auto-cutters).
- **End loss** at each end kept small; **splice** points marked so joins happen
  between pieces, not through them.
- Roll ends and faults: cut out faults at splice zones per the fabric fault policy.
- Keep a **lay record**: rolls, shade, plies per roll, ends — needed for reconciliation.

## 4. Cutting
- **Auto-cutter** (Gerber Paragon/Lectra Vector-type): vacuum hold-down with plastic
  overlay, knife sharpening interval, cutting speed and **overcut/knife intelligence**
  settings per material. Check the first pieces of a new material by measuring.
- **Straight knife** (manual): keep the knife vertical — tilt makes top and bottom
  plies different sizes. Blade sharp.
- **Notches** and **drill holes**: correct depth (too deep shows through the seam
  allowance on the garment), accurate position — sewing relies on them.
- Check sizes: measure panels from top, middle and bottom of the lay against the
  pattern.

## 5. Numbering and bundling
- Number each ply's panels (sticker/ticket) so all panels of one garment come from the
  same ply → same shade.
- **Bundle tickets** with style, size, colour, ply range, bundle number; bundles sized
  per the sewing line's system.
- Reconcile: pieces cut vs ordered, fabric used vs planned (consumption report).

## Gotchas
- Fusible panels (interlining) cut and fused before shrinkage → distortion; check fused
  panel size after the fusing press.
- Static and slippery fabrics (polyester linings) shift under the cutter — use paper
  between plies or lower ply height.

## Verify
- [ ] Marker efficiency at or above target; grain/nap rules respected.
- [ ] Fabric relaxed; shrinkage lot matches the pattern allowance.
- [ ] One shade per lay or numbered; lay record complete.
- [ ] Top/middle/bottom panels within tolerance; notches correct.
- [ ] Bundles ticketed and reconciled to the cut order.

*Draft: relaxation times and tolerances vary by fabric and customer; numbers given are
common starting points only.*
