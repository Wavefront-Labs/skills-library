---
id: architecture-construction.architecture.revit.view-templates-and-worksharing-setup
name: view-templates-and-worksharing-setup
category: architecture-construction
field: architecture
product: revit
tags: [revit, bim, autodesk, rvt, worksharing, worksets, central-model, local-model, synchronize-with-central, bim-360, acc, autodesk-construction-cloud, cloud-worksharing, view-templates, visibility-graphics, vg, phasing, phase-filters, levels, grids, project-base-point, survey-point, shared-coordinates, linked-models, families, schedules, sheets, project-browser, model-health, warnings, purge-unused]
level: practitioner
status: draft
description: "Set up a Revit architectural model a team can live in: levels/grids/coordinates, worksets and central model, view templates, phasing, browser organisation and model-health habits."
sources: ["Autodesk Revit help: worksharing, view templates, shared coordinates, phasing", "Common office BIM execution plan practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Revit project setup: view templates and worksharing

**Goal:** a Revit model that several people can edit at once without overwriting each
other, whose views look the same on every sheet, and that coordinates with consultants'
models — set up in the first day, because most of it is painful to retrofit.

## 1. Start from the office template
`.rte` templates carry families, line styles, view templates, title blocks and
schedules. Starting from the out-of-box template means rebuilding all of this later.

## 2. Levels, grids, coordinates (do these first, then pin them)
- Create levels with elevations from the brief; untick "Building Story" for non-floors
  (e.g. top of parapet) so they don't clutter schedules and exports.
- Draw grids; **pin** levels and grids (`PN`) — an accidental drag moves every hosted wall.
- Coordinates: the **Survey Point** represents the real-world (site) datum, the
  **Project Base Point** the building's local origin. Link the site/survey model and use
  *Acquire Coordinates* or *Publish Coordinates* so every discipline shares one system.
  Agree this in the BIM execution plan; mismatched coordinates are the most common
  federation error in Navisworks/clash detection.
- Set True North vs Project North so plans read orthogonal while site plans are true.

## 3. Worksharing
1. *Collaborate › Collaborate* — choose network (central file on a server) or cloud
   (Autodesk Docs / BIM Collaborate Pro).
2. Worksets: keep them few and meaningful — `Shared Levels and Grids`, `Exterior`,
   `Interior`, `Core`, `Furniture`, one per linked model (`Link - Structure`). Worksets
   are for **loading/visibility and ownership**, not a substitute for categories.
3. Each user creates a **local copy** (Revit does this when opening from central;
   don't copy the central file manually).
4. Habits: *Synchronize with Central* every 30–60 min and before leaving; *Relinquish
   all mine* at end of day; never "Save As" the central under a new name mid-project.
5. Element borrowing: if you can't edit something, *Place Request* to the owner rather
   than detaching.
6. Detach from central (with *Preserve worksets*) for audits or issue archives only.

## 4. View templates
- Build templates per view purpose: `Plan - GA 1:100`, `Plan - Furniture`, `RCP`,
  `Section 1:50`, `Elevation`, `Detail 1:5`, `Working - Coordination`.
- A template controls V/G overrides, detail level, scale, phase and phase filter,
  view range, filters. Assign it with **View Template** in properties (not *Apply
  Template Properties*, which is a one-off copy) so later template edits propagate.
- Use view **filters** (by parameter: fire rating, workset, phase) for colour-coded plans.
- Keep a parameter like `View Use` / `Sheet Series` for browser organisation.

## 5. Phasing
Set phases (*Existing*, *New Construction*, possibly *Demolition* handled via
"Phase Demolished") in *Manage › Phases*. Every element has Phase Created/Demolished,
every view a Phase and Phase Filter (`Show Complete`, `Show Previous + New`, etc.).
Most "wall disappeared" questions are a view on the wrong phase.

## 6. Families and loading
Prefer loadable families with type catalogues; avoid in-place families except for
genuinely one-off geometry (they're heavy and can't be scheduled consistently).
Nested shared families allow scheduling sub-components.

## Model health
- Watch the **warnings** count (*Manage › Review Warnings*) — overlapping walls,
  duplicate instances, room separation issues. Hundreds of warnings slow the model.
- *Purge Unused* (run more than once) before issue; *Audit* when opening a troubled
  central.
- Keep file size reasonable (as a rough office heuristic, investigate above several
  hundred MB) — usually CAD imports (import instead of link — always **link** DWGs),
  in-place families, or excessive groups. *Heuristic, varies by project.*
- Close hidden views; open the model to a lightweight starting view.

## Verify
- [ ] Levels and grids pinned; coordinates match the survey/consultant models.
- [ ] Central model on network/cloud; each user works in a local, syncs regularly.
- [ ] Every sheet view has an assigned (not applied) view template.
- [ ] Phase and phase filter correct on demolition and new-work plans.
- [ ] Warnings reviewed; no imported (vs linked) DWGs; purge run before issue.
