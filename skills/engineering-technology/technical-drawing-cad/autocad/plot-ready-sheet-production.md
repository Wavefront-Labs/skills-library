---
id: engineering-technology.technical-drawing-cad.autocad.plot-ready-sheet-production
name: plot-ready-sheet-production
category: engineering-technology
field: technical-drawing-cad
product: autocad
tags: [autocad, autocad-lt, bricscad, draftsight, 2d-drafting, layouts, paper-space, model-space, viewports, mview, annotative, annotation-scale, cannoscale, ltscale, psltscale, msltscale, page-setup, pagesetup, plot, publish, dwg-to-pdf, ctb, stb, plot-styles, lineweights, layers, xref, blocks, attributes, purge, audit, overkill, etransmit, iso-128, sheet-set]
level: practitioner
status: draft
description: "AutoCAD layouts to PDF: page setups, viewports at locked scales, annotative text/dims, LTSCALE/PSLTSCALE/MSLTSCALE, xref/layer hygiene, PURGE/AUDIT, PLOT/PUBLISH."
sources: ["Autodesk AutoCAD Help: annotative objects, layouts and viewports, PUBLISH, system variables reference"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plot-ready sheet production in AutoCAD

**Goal:** a model drawn once at full size, presented on correctly scaled layout sheets
whose text, dimensions and linetypes read the same at every viewport scale, and a
clean multi-sheet PDF out the other end.

## 1. Model space: full size, layered, nothing scaled
1. Draw everything at 1:1 in real units (check `INSUNITS` = 4 for mm). Never scale
   geometry to "fit" a sheet; scaling happens in viewports.
2. Put every object on a named layer (`LAYER`, alias `LA`), with colour, linetype and
   lineweight set **ByLayer**. A workable mechanical scheme (ISO 128 weights):
   `OUTLINE` 0.50, `HIDDEN` 0.25 dashed, `CENTRE` 0.25 chain, `DIM` 0.25, `HATCH` 0.18,
   `TEXT` 0.25 (heading text 0.35), `BORDER` 0.70, `VPORT` non-plotting.
   Keep it in your `.dwt`.
3. Repeated items are blocks (`BLOCK`/`B`, insert with `INSERT`/`I`). Title-block
   fields are attributes (`ATTDEF`); after editing a block definition run `ATTSYNC` or
   existing inserts keep the old attribute layout.
4. Reference other disciplines' drawings with `XREF` (`XR`), path type **Relative**.
   Prefer **Overlay** to Attach so nested references don't come back circularly.
   Keep `VISRETAIN` = 1 so overrides of `xref|layer` layers survive reloads.

## 2. Annotative scaling (set once, then forget about scale factors)
1. Text style: `STYLE`, tick **Annotative**, paper height 2.5 mm (general notes and
   dimensions), 3.5 mm (view titles), 5 or 7 mm (drawing number).
2. Dimension style: `DIMSTYLE` > Modify > Fit > **Annotative**; arrows 2.5, text 2.5,
   likewise for multileader styles.
3. Linetype variables, for an ISO/mm template using `acadiso.lin`:
   - `LTSCALE` = 1 (global factor; leave it alone once set)
   - `PSLTSCALE` = 1 (linetypes in viewports scaled by viewport scale)
   - `MSLTSCALE` = 1 (linetypes in the Model tab scaled by annotation scale)
   Then `REGENALL`; continuous-looking dashes after a change usually mean a missing regen.
4. Before annotating in model space set `CANNOSCALE` to the scale of the viewport
   that will show it (e.g. `1:5`). An annotative object only appears in viewports whose
   annotation scale it carries; add or remove scales with `OBJECTSCALE`.

## 3. Layouts and viewports
1. One layout tab per sheet, renamed to the sheet number (`A-101`, `DET-01`), because
   `PUBLISH` uses the layout name.
2. Insert the title block at 0,0 at 1:1 in paper space on `BORDER`.
3. Create viewports with `MVIEW` (`MV`) on layer `VPORT`. Set the scale from the
   status-bar scale list or Properties > Standard scale (1:1, 1:2, 1:5, 1:10, 2:1
   mechanical; 1:50/1:100 building).
4. **Lock** each viewport (Properties > Display locked = Yes) immediately. An unlocked
   viewport gets nudged by a wheel zoom and silently goes off-scale.
5. Hide layers per viewport with the **VP Freeze** column in the Layer Properties
   palette (or `VPLAYER`), not by global freeze.

## 4. Page setup and plotting
1. `PAGESETUP` > New, named e.g. `PDF-A3`: printer **DWG To PDF.pc3**, paper
   ISO full bleed A3 (420 x 297 mm), plot area **Layout**, scale **1:1**, plot style
   table `monochrome.ctb` (or your company `.ctb`/`.stb`), tick *Plot with plot
   styles*. Import it into other drawings from the Page Setup Manager.
2. `.ctb` vs `.stb`: a drawing is one or the other (`PSTYLEMODE`, read-only; convert
   with `CONVERTPSTYLES`). Don't mix company templates of different modes.
3. Single sheet: `PLOT` (Ctrl+P). Set: `PUBLISH`, load all layouts, save the list as a
   `.dsd`, output a **multi-sheet PDF**. Sheet Set Manager (`SHEETSET`) adds
   field-driven sheet numbers and an index.

## 5. Clean before issue or `ETRANSMIT`
1. `AUDIT`, answer **Y** to fix errors. If the file won't open cleanly, `RECOVER`.
2. `OVERKILL` removes duplicate/overlapping lines (inspect; it can over-merge).
3. `PURGE` (`PU`): tick nested items, include regapps and zero-length geometry. Repeat
   until nothing is left to purge.
4. Bloated scale list from imported xrefs: `-SCALELISTEDIT` > Reset.
5. Send with `ETRANSMIT` so xrefs, fonts and plot styles travel together.

## Worked mini-example
A 600 mm bracket on A3: main view 1:5 (120 mm on paper), detail 1:2. Annotative
2.5 mm text prints 2.5 mm in both (12.5 and 5 mm in model space). Detail dims carry
only the 1:2 scale, so they don't clutter the main view.

## Gotchas
- `ANNOAUTOSCALE` positive adds every new annotation scale to all annotative objects;
  it causes clutter; many CAD managers keep it negative (off).
- Lineweights not showing on screen is just `LWDISPLAY` off; the PDF uses them anyway.
- Fonts substituted on another machine: use TrueType or ship SHX via `ETRANSMIT`.

## Verify
- [ ] Every viewport shows a standard scale and is locked.
- [ ] Text and dimensions measure 2.5/3.5 mm on the printed PDF in every viewport.
- [ ] Hidden and centre lines show dashes at all scales after `REGENALL`.
- [ ] `AUDIT` reports 0 errors; `PURGE` has nothing left.
- [ ] `PUBLISH` produced one PDF with sheets in order and named after the layouts.
