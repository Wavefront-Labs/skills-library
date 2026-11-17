---
id: architecture-construction.architecture.archicad.project-setup-and-teamwork
name: project-setup-and-teamwork
category: architecture-construction
field: architecture
product: archicad
tags: [archicad, graphisoft, bim, pln, tpl, teamwork, bimcloud, bimcloud-basic, reserve-release, send-receive, stories, layers, layer-combinations, pen-sets, model-view-options, mvo, graphic-overrides, renovation-filter, view-map, layout-book, publisher-sets, gdl, library-manager, hotlinks, ifc, ifc-translator, open-bim, project-template, attributes]
level: practitioner
status: draft
description: "Set up an Archicad project the Graphisoft way: template and attributes, stories, layer combinations, view map, layout book, publisher sets and Teamwork reserve/send/receive habits."
sources: ["Graphisoft Archicad help: Navigator (Project Map, View Map, Layout Book, Publisher)", "Graphisoft BIMcloud / Teamwork documentation", "Graphisoft IFC translator documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Archicad project setup and Teamwork

**Goal:** a project file where every drawing is a saved *view* of one model, sheets
update themselves, and several people can work at once — using Archicad's own
structure (Project Map → View Map → Layout Book → Publisher) rather than fighting it.

## 1. Template and attributes
Start from the office `.tpl`. Archicad's **attributes** (layers, pens and pen sets,
line types, fills, composites, building materials, profiles, surfaces, zone
categories) live in the project, not the library. Manage them in *Attribute Manager*
and import them between projects there; never re-create a composite by hand in each job.

**Building materials** are the key attribute: they hold cut fill, surface and
**intersection priority**, which decides how walls, slabs and beams join. Wrong
priorities produce the familiar "slab line through the wall in section" mess.

## 2. Stories
Set stories in *Design › Story Settings*. Elements belong to a *home story*;
"show on stories" controls display above/below. Keep stories to real floors; use
reference levels for things like top of parapet.

## 3. The four Navigator maps
1. **Project Map** — raw viewpoints: stories, sections, elevations, details, 3D, schedules.
2. **View Map** — *saved views*: a viewpoint plus a stored state of **layer
   combination, scale, pen set, Model View Options (MVO), graphic override, renovation
   filter, structure display, dimension style and zoom**. Drawings on sheets come from here.
3. **Layout Book** — sheets (layouts) on master layouts with title blocks; drag views
   in as drawings. Drawings are live links; set them to *auto-update*.
4. **Publisher** — publisher sets for PDF/DWG/IFC/print issues; save one per issue type
   (e.g. `Planning PDF`, `Consultant DWG`, `IFC Coordination`).
Discipline: always build a view, then place the view. Placing from the Project Map
gives a drawing whose look changes when someone else toggles layers.

## 4. Layers and combinations
Layers control visibility and locking; **layer combinations** are named on/off sets
(`01 GA Plan`, `02 Furniture`, `03 RCP`). Graphic overrides (since Archicad 23) handle
colour-coding by rule — prefer them over duplicating layers for presentation.

## 5. Renovation
Every element has a renovation status: *Existing*, *To Be Demolished*, *New*. The
**renovation filter** saved with each view decides what shows and how (e.g. demolition
dashed). Set the status at placement; changing it afterwards for hundreds of elements
is slow.

## 6. Teamwork
- Share the project to **BIMcloud** (or BIMcloud Basic for small teams).
- **Reserve** elements or whole stories/layers before editing; *Release* when done.
  Unreserved elements are read-only to you.
- **Send & Receive** frequently — small, frequent sends keep conflicts low and the
  server copy current.
- Use the Messages/Requests panel to ask a colleague to release an element.
- Library parts live in BIMcloud libraries; *Library Manager* must report no missing
  objects (missing GDL parts show as dots in plan).

## 7. Exchange
- Hotlinks (`.pln`/`.mod`) for repetitive units or modules — edit the source once.
- IFC export via the **IFC translator**; check classifications and property mapping
  (Pset_WallCommon etc.) with the receiving consultant, and open the IFC in a viewer
  before sending.
- DWG export uses a DWG translator; set layer mapping to match the receiver's standard.

## Gotchas
- Pens are numbered; a pen set swap changes all line weights in that view — check the
  pen set saved in the view before blaming the element.
- "Model View Options" can hide door swings or show simplified walls — check MVO first
  when something looks wrong in one view only.
- Version upgrades are one-way; agree the Archicad version for the team before sharing.
- Specific menu names move between versions (e.g. Attribute Manager was redesigned);
  *verify paths in your version.*

## Verify
- [ ] Every placed drawing comes from the View Map, not the Project Map.
- [ ] Building-material priorities give clean wall/slab junctions in a test section.
- [ ] Renovation filter correct on existing/demolition/new views.
- [ ] Library Manager shows no missing parts; Teamwork send/receive works for all users.
- [ ] Publisher set produces the full issue in one run.
