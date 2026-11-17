---
id: creative-arts.film-live-action.final-draft.tag-mode-and-breakdown-export
name: tag-mode-and-breakdown-export
category: creative-arts
field: film-live-action
product: final-draft
tags: [final-draft, film-live-action, screenwriting-software, script-reports, scene-report, character-report, location-report, cast-report, tagging, tagger, tag-mode, breakdown-export, breakdown, movie-magic-scheduling, scenechronize, scheduling-export, sex, fdx, csv-export, production-prep, eighths, character-report-fd, cast-list-report, location-report-fd, scene-list-report, tag-categories, custom-tags, export-to-scheduling, sex-export, script-statistics, statistics-report]
level: practitioner
status: draft
description: "Pull production data out of Final Draft: scene, character, location and cast reports, Tag Mode to mark props/wardrobe/stunts per scene, and exporting a breakdown to Movie Magic Scheduling."
sources:
  - "https://www.finaldraft.com/support/ (Final Draft 12/13 user guides - Reports, Tag Mode, Export)"
  - "https://kb.finaldraft.com/ (Tagging and exporting to scheduling software)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag Mode, reports and breakdown export in Final Draft

**Goal:** stop re-typing the script into spreadsheets. Final Draft already knows every
scene, speaker and location; make it produce the paperwork the AD and line producer need,
and tag breakdown elements once so they flow into scheduling software.

## 1. Prerequisites
- Scene headings must be real `Scene Heading` elements (not Action in caps). Check with
  the Navigator (`Tools > Navigator > Scenes`): any slug missing from the list is mis-elemented.
- Character names consistent - `MARTA` and `MARTA (V.O.)` are the same character; `MARTHA`
  is not. Use the Characters navigator to spot variants.
- Apply **Scene Numbers** (`Production > Scene Numbers`) before exporting; scheduling
  software keys everything to the number.

## 2. Reports (`Tools > Reports`)
| Report | Use |
|---|---|
| **Scene Report** | Scene number, heading, page length (eighths), first line - the raw one-liner schedule. Tick "include eighths". |
| **Location Report** | Scenes grouped by location, with INT/EXT and time of day - for the location manager. |
| **Character Report** | Every character, scenes they appear in, speech counts - for casting and day-out-of-days. |
| **Cast Report** | Per-scene cast list. |
| **Script Report** | Page counts, element statistics, estimated running time. |
| **Statistics** | Dialogue vs action percentage, longest speech - sanity-check a talky draft. |
Reports open as a new document; `File > Save As` to PDF/FDX or copy to a spreadsheet.
Page lengths are in **eighths** of a page - the scheduling unit.

## 3. Tag Mode (`Production > Tag Mode`)
1. Enter Tag Mode; text becomes read-only, tags editable.
2. Select a word or phrase (e.g. "revolver"), choose a category in the Tags panel:
   Cast, Extras, Stunts, Vehicles, Props, Special Effects, Wardrobe, Makeup/Hair, Animals,
   Sound, Music, Set Dressing, Greenery, Special Equipment, Security, Additional Labour, VFX,
   Mechanical Effects, Notes - or add custom categories.
3. Tagged text is highlighted by category colour; the **Tags List** shows all tags grouped
   by scene and category. Tag the first mention per scene - elements are scene-scoped.
4. Speaking characters are auto-tagged as Cast from dialogue cues; add non-speaking
   characters by tagging their name in action.
5. Exit Tag Mode; tags persist in the `.fdx` and travel with revisions. They are anchored to
   text, so a page-one rewrite can orphan tags - re-check the Tags List afterwards.

## 4. Exporting the breakdown
- **Movie Magic Scheduling:** `File > Export > Movie Magic Scheduling (.sex)` or import the
  `.fdx` directly in MMS 6+ (`File > Import > Final Draft`). Tagged elements arrive as
  breakdown-sheet elements; scene numbers and eighths carry across.
- **Scenechronize / StudioBinder / Celtx:** import `.fdx` directly; verify tag mapping.
- **Spreadsheet:** save the Scene Report and Tags List as text, or
  `File > Export > Text (Tab Delimited)`; open in Excel and pivot by scene.
- Always export from the **locked, scene-numbered production draft**. Re-export after
  coloured-page revisions and diff the scene list (omitted and A-scenes).

## Gotchas
- Reports count by element type: a `Transition` element containing a slug is invisible.
- Dialogue cues with typos create phantom characters that bloat the Cast report.
- Tagging before scene numbers are locked - tags survive, but the schedule built from
  the old numbers breaks.
- `(CONT'D)` and `(V.O.)` are handled; a cue like `MARTA'S VOICE` is a new character.

## Verify
- [ ] Navigator scene list matches the script's slugs; no phantom characters.
- [ ] Scene numbers applied and locked before tagging/export.
- [ ] Tags List shows every scene with Cast tagged; props/stunts/vehicles tagged where present.
- [ ] Imported breakdown shows the correct scene count and eighths.
