---
id: architecture-construction.architecture.autocad.architectural-drawing-setup
name: architectural-drawing-setup
category: architecture-construction
field: architecture
product: autocad
tags: [autocad, autocad-lt, dwg, cad, drafting, architectural-drafting, layers, layer-standards, aia-cad-layer-guidelines, ncs, bs-1192, iso-13567, xref, external-reference, model-space, paper-space, layouts, viewports, annotative, annotation-scale, dimstyle, plot-style, ctb, stb, sheet-set-manager, title-block, units, drawing-template, dwt, purge, audit, etransmit]
level: practitioner
status: draft
description: "Set up an architectural AutoCAD drawing set that survives a project: 1:1 model space, layer standard, xref structure, annotative scales, layouts/viewports, plot styles and sheet sets."
sources: ["Autodesk AutoCAD help: xrefs, annotative objects, sheet set manager", "US National CAD Standard / AIA CAD Layer Guidelines", "ISO 13567 / BS 1192 layer naming"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Setting up an architectural drawing set in AutoCAD

**Goal:** a DWG set where plans, sections and details stay consistent as the design
changes — one source of geometry, predictable layers, text that prints the right size
at any scale, and sheets that plot identically every time.

## 1. Start from a template, not a blank file
- Create or obtain an office `.dwt` holding: units, layers, text and dimension styles,
  plot styles, a title-block layout. `UNITS`: architectural (feet-inches) or decimal
  millimetres — decide once; mixing mm and m files is the classic 1000× xref bug.
- Set `INSUNITS` so blocks and xrefs scale correctly when inserted across files.
- Draw **everything in model space at 1:1** (full size). Scale belongs to viewports,
  never to geometry.

## 2. Layer standard
Use a published convention rather than inventing one:
- US: NCS / AIA style `A-WALL`, `A-DOOR`, `A-GLAZ`, `A-ANNO-DIMS`, `A-FLOR-FIXT`.
  Discipline letter, major group, optional minor group and status (`-NEWW`, `-DEMO`, `-EXST`).
- UK/EU: ISO 13567 / Uniclass-based codes, often required by clients on BIM projects.
Rules that matter more than the scheme: objects drawn **ByLayer** for colour,
linetype and lineweight; layer 0 only inside block definitions; never draw on
`Defpoints` (it does not plot — a common "where did my lines go" moment).
Save layer states (`LAYERSTATE`) for "demolition plan", "furniture plan", "RCP".

## 3. Xref structure (the backbone)
- One **base model per floor** (walls, doors, windows, core) as its own DWG.
- Sheet files *xref* the base, attach title blocks, and add annotation only.
- Attach xrefs with **relative paths** and `Overlay` (not `Attach`) for
  background files, so nested references don't chain into other people's sheets.
- Use `XREF` palette to watch for "Not Found" and "Needs reloading".
- Control xref layer visibility per viewport with `VPLAYER`/layer properties VP Freeze —
  set `VISRETAIN=1` so host overrides survive reloads.
- Coordinate system: insert all floor xrefs at **0,0,0** on a shared grid origin; agree
  this before the first wall is drawn. Moving a base file later breaks every sheet.

## 4. Annotation that scales
- Make text styles, dimension styles, hatches and tags **annotative**. Add the
  annotation scales you actually use (1:100, 1:50, 1:20 / 1/8", 1/4", 1-1/2").
- Set the viewport scale first, then annotate *through* it, or set `CANNOSCALE` in
  model space. Check `ANNOALLVISIBLE` if text seems to vanish at another scale.
- Typical paper text heights: 2.5 mm body / 3.5 mm titles (≈ 3/32" and 1/8").

## 5. Layouts, viewports and plotting
- One layout per sheet; title block as a block with attributes or fields.
- Lock viewports after setting scale (`Display Locked = Yes`) — an accidental zoom
  inside an unlocked viewport silently rescales the sheet.
- Lineweights come from a **CTB** (colour-dependent) or **STB** (named) plot style;
  most offices are still CTB. Match the template — mixing both needs `CONVERTPSTYLES`.
- Page setups saved in the template; plot to PDF with the same setup every time.

## 6. Sheet Set Manager
For more than a handful of sheets, use `SHEETSET`: sheet numbers and titles live as
properties, title blocks pull them through fields, and you can publish the whole set
to multi-sheet PDF and generate a sheet list table. Renumbering then becomes one edit.

## Gotchas
- **Exploding** dimensions or hatches breaks associativity — avoid.
- Files that grow and slow down: run `PURGE` (incl. registered apps) and `AUDIT`;
  `-PURGE` regapps clears junk imported with consultant files.
- Sending files: use `ETRANSMIT` so xrefs, fonts and plot styles travel together.
- SHX vs TrueType fonts behave differently in PDF search and in LT; follow the template.
- AutoCAD LT lacks some automation (no LISP in older LT versions; LT 2024+ added
  limited AutoLISP) — confirm before relying on office routines. *Unverified for every
  LT release.*

## Verify
- [ ] Geometry is 1:1 in model space; `UNITS`/`INSUNITS` match all xrefs.
- [ ] Every object is ByLayer on a standard layer; nothing on `Defpoints` or 0.
- [ ] All floor xrefs share 0,0,0 and use relative paths.
- [ ] Text measures the intended paper height in every viewport scale.
- [ ] Viewports locked; a test PDF plot matches lineweight expectations.
- [ ] `ETRANSMIT` package opens cleanly on another machine.
