---
id: architecture-construction.construction-estimating-scheduling.bluebeam-revu.calibrated-takeoff-with-measurement-tools
name: calibrated-takeoff-with-measurement-tools
category: architecture-construction
field: construction-estimating-scheduling
product: bluebeam-revu
tags: [construction-estimating-scheduling, bluebeam-revu, bluebeam, revu, pdf-takeoff, digital-takeoff, on-screen-takeoff, quantity-takeoff, measurement-tools, calibrate, scale, viewports, length, polylength, area, count, volume, tool-chest, markups-list, custom-columns, csv-export, quantity-link, estimating, measure, overlay]
level: practitioner
status: draft
description: "Do a reliable quantity takeoff in Bluebeam Revu: calibrate scale per viewport, measure length/area/count, use Tool Chest presets and the Markups List to export quantities."
sources: ["Bluebeam Revu online help (Measurements, Calibrate, Viewports, Markups List)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibrated takeoff with Bluebeam Revu measurement tools

**Goal:** measure quantities from PDF drawings in Revu so that every number is on the
right scale, labelled consistently, and exportable to the estimate — with a check that
catches the classic scale error before it reaches the bid.

## 1. Prepare the set
1. Combine or open the sheets; check each page is **vector** (zoom in hard — crisp lines
   and selectable text) rather than a scan. Scans measure fine but snapping won't work.
2. Rename pages to sheet numbers (Thumbnails panel) — the Markups List *Page Label*
   column is your audit trail.
3. Note the scale(s) printed on each sheet and in each detail. One sheet can hold a 1:100
   plan and a 1:20 detail; US sheets mix 1/8" = 1'-0" and 1/4" = 1'-0".

## 2. Set scale correctly (the step that ruins estimates)
- **Calibrate**, don't trust the preset. Measurements panel (`Alt+U`, unverified
  shortcut) › Calibrate › click two ends of a long known dimension (a gridline-to-gridline
  dimension, ideally > 10 m / 30 ft) › enter the true value. Longer reference = smaller
  error.
- Use **Viewports** where a sheet has multiple scales: draw a viewport around each
  detail and give it its own scale. Measurements inside take that viewport's scale.
- Apply the scale to **all pages with the same scale** via the page range option in the
  calibrate dialog — then spot-check a second sheet.
- Sheets printed "NTS" or reduced to A3/11x17: calibrate from a dimension, never the
  title block scale.

## 3. Measure
| Tool | Shortcut (default) | Use |
|---|---|---|
| Length | `Shift+Alt+L` | single runs |
| Polylength | `Shift+Alt+N` | walls, kerbs, pipe runs |
| Area | `Shift+Alt+A` | slabs, flooring, roofing |
| Perimeter | `Shift+Alt+P` | skirting, edge forms |
| Count | `Shift+Alt+C` | doors, fixtures, piles |
| Volume | `Shift+Alt+V` | area × depth for concrete, excavation |
(Shortcuts unverified — they vary between Revu versions and can be remapped.)
- Turn on **Snap to Content** and **Snap to Markup** (status bar toggles).
- **Area cutouts**: right-click while drawing an area › add a cutout for voids, or use
  the Cutout tool afterwards — don't measure gross and forget to deduct.
- For walls, set **Depth/Height** in the measurement's properties so Revu reports wall
  area or volume as well as length.

## 4. Make the tools do the bookkeeping
- Build **Tool Chest** presets per item: e.g. "Blockwork 190 – 2.7 m high", colour,
  hatch, subject, layer, and depth already set. Set them to **Properties mode** (drawn
  markups take the saved properties). Everyone on the team then takes off identically.
- Add **custom columns** in the Markups List (Markups List › Columns › Manage Columns):
  e.g. trade code, waste %, formula columns such as `Area * 1.10` for waste-adjusted
  quantities (formula syntax unverified — check help for your version).
- Use the **Subject** field as the cost code. Group the Markups List by Subject to see
  totals.

## 5. Export and link
- Markups List › **Summary** › CSV/XLSX to send quantities to the estimate spreadsheet.
- **Quantity Link** (Revu eXtreme / higher tiers, unverified per licence) pushes totals
  live into Excel cells, so later revisions update the estimate.
- When a revised set arrives, use **Overlay Pages** or **Compare Documents** to find
  changes, then re-measure only the clouded areas.

## Gotchas
- One wrong calibration = every quantity on that page wrong by the same factor; the
  totals look plausible.
- Measuring across a viewport boundary uses the scale where you started.
- Copy/pasting measurements between pages with different scales keeps the markup but
  recalculates with the target page's scale — check.
- Hidden layers still count in the Markups List; filter by status or layer.
- Don't measure from the PDF dimension text alone; dimensions and drawn geometry
  sometimes disagree — query the designer, note the RFI.

## Verify
- [ ] Each page/viewport scale was calibrated or checked against a known dimension.
- [ ] A test length (e.g. a grid spacing) measures within ~0.5% of its dimension.
- [ ] Every markup has a Subject/cost code and appears in the Summary export.
- [ ] Areas show deductions for voids; walls carry height.
- [ ] Totals reconcile with a rough check (e.g. floor area × typical ratio).
