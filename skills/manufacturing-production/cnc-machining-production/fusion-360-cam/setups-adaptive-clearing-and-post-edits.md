---
id: manufacturing-production.cnc-machining-production.fusion-360-cam.setups-adaptive-clearing-and-post-edits
name: setups-adaptive-clearing-and-post-edits
category: manufacturing-production
field: cnc-machining-production
product: fusion-360-cam
tags: [fusion-360-cam, fusion-360, autodesk-fusion, fusion-manufacture, cam, cnc-programming, setup, wcs, stock, work-offset, adaptive-clearing, 3d-adaptive, 2d-adaptive, hsm, rest-machining, optimal-load, tool-library, feeds-and-speeds, simulation, stock-simulation, post-processor, cps, post-library, javascript-post, nc-program, templates, turning, fixtures, cnc-machining-production]
level: practitioner
status: draft
description: "Program parts in Fusion 360 Manufacture: setups with correct WCS and stock, adaptive clearing with optimal load, rest machining, simulation with holders and fixtures, and editing .cps posts safely."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setups, adaptive clearing and post edits in Fusion 360 CAM

**Goal:** Fusion (Autodesk Fusion, formerly Fusion 360) programs that hold the right
work offset, rough fast with Adaptive Clearing, verify against fixtures, and post
code the machine runs unchanged.

*Draft: from Fusion releases 2023–2025. Some features (machine simulation, some
multi-axis and probing tools) need the Manufacturing Extension; the personal-use
licence has posting/rapid limitations — check your licence.*

## 1. Setup
- **One setup per fixture/orientation.** Set **WCS orientation** and **origin** to what
  the setter will touch off (e.g. stock top, vice fixed-jaw corner). An origin at
  "model origin" by default is the classic wrong-offset crash.
- **Work offset** number in the setup's Post Process tab (0/1 → G54, 2 → G55 …; mapping
  depends on the post — confirm in the output).
- **Stock:** relative size box or from a solid body (castings, previous-op stock).
  For op 2, use **"From preceding setup"** so rest machining knows what's left.
- Model **fixtures** (vice jaws, clamps) as bodies and select them in the setup so
  simulation can flag collisions.
- Use the **machine** definition (if you have one) for axis limits and post selection.

## 2. Adaptive Clearing
- **Optimal load** (radial engagement): start ~10–15% of tool diameter for hard materials,
  up to ~25–40% in aluminium on rigid machines; **maximum roughing stepdown** up to the
  usable flute length. The tool vendor's HEM data beats these rules of thumb.
- Raise feed for chip thinning at low engagement (the vendor calculators do this).
- **Stock to leave**: radial and axial (e.g. 0.2–0.3 mm) for finish passes.
- **Ramp type** helix with a modest angle; check **minimum cutting radius** to avoid
  slotting at the core.
- **Rest machining** with "from previous operation(s)" stock for a smaller tool to clear
  corners only.
- **Both ways** vs climb only: climb is default; leave it unless you know why.

## 3. Finishing
- 2D Contour for walls (one or two passes with a spring pass if needed), Face/Pocket
  floors with a separate operation. 3D: Scallop/Parallel/Steep and Shallow, with
  stepover from the target scallop height.

## 4. Tool library
- Use a **cloud/document tool library** for the shop with real holders and stick-out,
  correct tool numbers matching the machine's carousel, and **presets** per material
  for feeds/speeds. A tool copied into a document doesn't update from the library —
  sync deliberately.

## 5. Simulation
- **Simulate with stock**, collisions on (holder, fixtures). Colour comparison shows
  excess stock and gouges.
- Check rapids that pass through fixtures at the **clearance/retract heights** — set
  them from the stock top plus margin, not from the model top only.

## 6. Posts (.cps)
- Posts are JavaScript files from the Autodesk post library. Choose the one for your
  control family (Fanuc, Haas, Heidenhain, Siemens, Mazak…) and machine.
- Use the **post properties** (in the NC program dialog) first: safe start, sequence
  numbers, coolant codes, tool preload, smoothing. Many needs are covered there.
- To edit: copy the post to your personal/cloud post library, edit in a code editor
  (VS Code has an Autodesk post extension), keep the original untouched, version
  the edited file with a changelog at the top.
- After editing, post a **standard test program** and diff against the previous output.

## Gotchas
- Editing the model after programming → toolpaths flagged (red/yellow); **regenerate**.
- Templates save time but carry old tool numbers — check after applying.
- Fusion's default heights reference "model top"; if stock is taller, rapids hit stock.
- An NC program object controls which ops are posted and in what order — check it.

## Verify
- [ ] WCS origin matches the setup sheet; correct G54+ in posted code.
- [ ] Simulation with fixtures shows no collisions; rest stock as expected.
- [ ] Tool numbers and lengths match the machine.
- [ ] Posted code read through for safe start, offsets and coolant.
- [ ] Edited posts versioned and diff-tested.
