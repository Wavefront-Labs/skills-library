---
id: computing-software.general-digital-literacy.office-suites.speaker-notes
name: speaker-notes
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slides, speaker-notes, notes-page, print-notes, notes-pane, script]
level: intro
status: docs-checked
description: "Write speaker notes, view them privately while presenting and print notes pages in PowerPoint, Google Slides and Impress."
sources:
  - https://support.microsoft.com/en-gb/powerpoint/training/add-speaker-notes-to-your-slides
  - https://support.microsoft.com/en-us/powerpoint/training/start-the-presentation-and-see-your-notes-in-presenter-view
  - https://support.microsoft.com/en-us/powerpoint/print-slides-with-or-without-speaker-notes
  - https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-deliver-powerpoint-presentations
  - https://support.google.com/docs/answer/1696787
  - https://support.google.com/docs/answer/1696717
  - https://support.google.com/docs/answer/143346
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/presenter_console.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/printing.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Speaker notes

**Goal:** keep your talking points with each slide, visible only to you.

## Write them
- **PowerPoint:** the Notes pane under the slide ("Click to add notes"); if it's hidden, click **Notes** on the
  status bar. Drag its top edge up for more room.
- **Google Slides:** the speaker notes panel under the slide (`Ctrl+Alt+Shift+S` opens it).
- **Impress:** View › Notes.
Write prompts, not a full script: keywords, a number to quote, the transition line to the next slide.

## See them while presenting
- PowerPoint **Presenter View** (used by default, set up automatically when a second screen is connected):
  notes, next slide and timer on your screen. With one screen, `Alt+F5` (Mac `Option+Return`) starts
  Presenter View for practice. You can edit notes and change their text size in Presenter View.
- Google Slides: next to **Slideshow** › drop-down › **Presenter view** › Speaker notes; `s` opens them during a show.
- Impress: the Presenter Console's **Notes** mode, with a second display connected.

## Print
PowerPoint File › Print › Full Page Slides › **Notes Pages** (the only layout that prints notes). Google Slides:
File › Print settings and preview › *1 slide with notes*. Impress: File › Print › Document: **Notes**.

## Gotchas
- Notes are inside the file: they travel when you share the deck. Remove private notes before
  sending (PowerPoint File › Info › Check for Issues › Inspect Document › *Presentation Notes*; it can't
  remove pictures in notes).

## Verify
- [ ] In a practice run your notes show on your screen only.

## Checked
2026-10-27, against Microsoft Support (Add speaker notes; Presenter view; Print with notes; Document Inspector; delivery keyboard shortcuts; PowerPoint for Microsoft 365 and 2016-2024), Google Docs Editors Help (Present slides; keyboard shortcuts; Print a file) and the LibreOffice help master branch (Presenter Console; printing guide). Confirmed: Notes pane and status-bar Notes button, Google notes shortcut and Presenter view path, Impress View › Notes and console Notes mode, Presenter View defaults and Alt+F5/Option+Return, Notes Pages as the only notes print layout, Google and Impress notes printing, and the Presentation Notes inspector with its picture limit. Removed an unconfirmed View › Notes Page claim and a PDF-export claim.
Method: documentation only; no commands were run.
