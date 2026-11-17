---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.page-manager-adding-reordering-and-spreads
name: page-manager-adding-reordering-and-spreads
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-comic-project, csp-page-management, csp-page-manager, story-file, spreads, page-template, cmc-file]
level: practitioner
status: draft
description: "Manage a multi-page CSP story: page manager window, adding/deleting/reordering pages, combining pages into spreads, page templates, and keeping story files healthy."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://www.clipstudio.net/en/functions/
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Page manager: adding, reordering and spreads

**Goal:** manage a whole issue in one CSP story file without broken pages or wrong
spreads.

## The story file
A multi-page work is a management file (.cmc) plus a folder of page files (.clip).
Keep them together; move/copy the whole folder, never individual page files.
(Multi-page works beyond a small page count require Clip Studio Paint EX.)

## Page manager window
Opens with the story; shows thumbnails in spread order according to binding.
- Double-click a thumbnail to open that page.
- **Story menu** (or right-click): Add page, Add page (Advanced) with template, Delete
  page, Combine into spread / Split spread, Change basic work settings (applies trim,
  bleed, resolution to all pages).
- **Reorder** by dragging thumbnails; page numbers update.
- Spreads: combine two facing pages into one spread page for double-page art; split
  back for export if the printer wants singles.

## Templates
Add pages with a template (frame layout material or saved page template) to start
each page with the standard grid and layers.

## Batch changes
Story > Change basic work settings for all pages; Edit > Batch process (EX) to run
operations or auto actions across pages.

## Gotchas
- Moving page files in the OS breaks the story; use CSP's commands.
- Combining pages with different settings fails; unify settings first.
- Changing binding after drawing flips spread order; decide at creation.

## Verify
- [ ] Page manager shows correct spread pairing and numbering.
- [ ] Story folder backed up as a whole.
