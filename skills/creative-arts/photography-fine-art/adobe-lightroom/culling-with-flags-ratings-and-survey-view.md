---
id: creative-arts.photography-fine-art.adobe-lightroom.culling-with-flags-ratings-and-survey-view
name: culling-with-flags-ratings-and-survey-view
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, culling-workflow, lightroom-library, pick-flags, star-ratings, survey-view, compare-view, lightroom-classic]
level: practitioner
status: draft
description: "Cull a shoot in Lightroom Classic in passes with pick/reject flags, star ratings, Auto Advance, Survey and Compare views, then remove rejects safely."
sources: ["https://helpx.adobe.com/ie/lightroom-classic/desktop/viewing-photos/browse-compare-photos.html", "https://helpx.adobe.com/lightroom-classic/desktop/help/library-module-basic-workflow.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Flag, label and rate photos)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Culling with flags, ratings and Survey view

## Setup
- Build 1:1 or Standard previews at import (or Library > Previews > Build 1:1) so zooming is instant.
- Turn on **Photo > Auto Advance** (or hold Shift with the key) so each keystroke moves on.
- Loupe view (`E`), hide panels (`Shift+Tab`), lights dim (`L`).

## Pass 1: reject (fast, one look each)
- `X` reject obvious failures (focus missed, eyes closed, blown exposure). `U` clears a flag. Do not rate yet.
- Then Photo > Delete Rejected Photos (Ctrl/Cmd+Backspace) > **Remove from Lightroom** (keeps files) or **Delete from Disk**. Prefer removing until your backup has run.

## Pass 2: picks
- Filter to Unflagged (Library Filter > Attribute or the filmstrip flag filter). `P` for anything worth a second look.

## Pass 3: compare similar frames
- **Survey** (`N`): select a burst; click the X on a frame to drop it from view until one or two remain. Zoom with the Navigator to compare focus.
- **Compare** (`C`): Select (left) vs Candidate (right) with linked zoom (lock icon). Promote the better frame with the "Make Select" button, then step through candidates.
- Stacking (`Ctrl/Cmd+G`, or Photo > Stacking > Auto-Stack by Capture Time) collapses bursts to the best frame.

## Pass 4: ratings
- `1-5` for strength: 3 = good, 4 = portfolio candidate, 5 = finished/exhibited. Keep 5 rare.
- Colour labels (`6-9`) for workflow state (red = needs retouch, green = print-ready), separate from quality.

## Gotchas
- Flags are global: a photo flagged in a collection is flagged in its folder too.
- Flags are not written to XMP for other apps; ratings and labels are.

## Verify
- [ ] Filter Flagged + Rating >= 3 gives the edit set you would show someone.
