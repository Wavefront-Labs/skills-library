---
id: creative-arts.literary-writing.scrivener.custom-metadata-fields
name: custom-metadata-fields
category: creative-arts
field: literary-writing
product: scrivener
tags: [literary-writing, scrivener, scrivener-3, scrivener-metadata, custom-metadata, metadata-fields, checkbox, list-field, date-field, outliner-columns, story-timeline, placeholders]
level: practitioner
status: draft
description: "Create Scrivener 3 custom metadata fields (text, checkbox, list, date) for story date, POV, plot thread or revision flags, show them as outliner columns."
sources: ["https://www.literatureandlatte.com/learn-and-support/user-guides"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom metadata fields

**Goal:** add your own structured fields to every document — beyond Label, Status and
Keywords — and work with them in the outliner like a spreadsheet. Scrivener 3 supports
several field types.

## Create fields
**Project > Project Settings > Custom Metadata**:
- **Text** — free text (e.g., "Scene goal", "Story date (text)", "Setting").
- **Checkbox** — yes/no flags ("Needs research", "Beta-read", "Has flashback").
- **List** — a dropdown of values you define ("Plot thread": A-plot, B-plot, Romance).
- **Date** — a real date field ("Story date"), sortable.
Set field titles, list values, defaults and text alignment there.

## Fill and view
- Inspector > **Metadata** pane shows the fields for the selected document.
- **Outliner:** add the fields as **columns** (column chooser) — edit inline, sort by
  clicking the header. A "Story date" date column sorted ascending gives you a
  chronological view even when the binder order is non-linear (flashbacks, dual timelines).

## Practical field sets
| Project type | Fields |
|---|---|
| Novel | POV (list), Story date (date), Scene goal (text), Turn (text), Plot thread (list) |
| Mystery | Clues planted (text), Suspects present (text), Reveals (checkbox) |
| Revision | Beta notes addressed (checkbox), Word count target met (checkbox) |
| Nonfiction | Sources verified (checkbox), Permissions needed (checkbox) |

## Searching and compile
- Project search can be scoped to specific metadata; save results as collections.
- Custom metadata can be inserted at compile with a placeholder (the manual lists the
  form, `<$custom:FieldName>` style) — useful for synopses or a scene list export. Verify
  the exact placeholder syntax in the Scrivener manual's placeholder list for your version.

## Gotchas
- Too many fields that you won't maintain — choose 3-6.
- Text fields for things you'll want to sort chronologically — use the Date type.
- Changing list values later: existing documents keep old values; update them.

## Verify
- [ ] Fields created with appropriate types.
- [ ] Outliner view with custom columns saved/used.
- [ ] Every scene has its key fields filled.
