---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.batch-processing-and-auto-actions-across-pages
name: batch-processing-and-auto-actions-across-pages
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-comic-project, csp-page-management, csp-batch-process, csp-auto-actions, multi-page, automation]
level: advanced
status: draft
description: "Automate repetitive work across comic pages in Clip Studio Paint: record Auto Actions, run File > Batch process on a story (EX), and combine with export settings safely."
sources:
  - https://tips.clip-studio.com/en-us/articles/9949
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch processing and auto actions across pages

## Auto Actions
- **Window > Auto action** opens the palette. Create a new set, click record, perform the steps
  (e.g. create a layer folder structure, set a layer to monochrome output, flatten-copy for export),
  stop recording.
- Play it on the current page with the play button or assign a shortcut. Some operations (dialogs with
  free input, certain tool strokes) are not recorded; test the action on a copy.
- Export/import action sets (`.caa` style files) to share with assistants.

## Batch process (EX)
- **File > Batch process** runs one auto action across selected pages of a story file, and can save or
  export each page afterwards.
- Choose pages (all or a range), the auto action, and whether to overwrite the page files, save as copies,
  or export (format and size like Export multiple pages).
- Typical uses: add a "Notes" layer to every page, set every tone layer to the same frequency, hide
  guide layers before export, convert all colour pages' expression colour.

## Safe workflow
1. Duplicate the story folder (or back it up) before overwrite runs.
2. Test the action on one page.
3. Run batch on a small range, check, then the full story.

## Gotchas
- Actions that depend on a selected layer behave differently on pages with different layer orders;
  standardise page templates first.
- Batch process with "overwrite" cannot be undone across pages.
- PRO has auto actions but no story-wide batch.

## Verify
- [ ] Spot-check first, middle and last pages after a run.
- [ ] Backup exists before any overwrite.
