---
id: computing-software.general-digital-literacy.office-suites.reusing-slides-from-another-deck
name: reusing-slides-from-another-deck
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slides, reuse-slides, import-slides, keep-source-formatting]
level: intro
status: docs-checked
description: "Pull slides from another presentation into PowerPoint, Google Slides or Impress with Reuse Slides, Import slides or Insert Slide from File, keeping or matching the theme."
sources:
  - https://support.microsoft.com/en-us/powerpoint/reuse-import-slides-from-another-presentation
  - https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks
  - https://support.google.com/a/users/answer/9282978
  - https://support.google.com/docs/answer/7009814
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/00/00000404.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reuse slides from another deck

## PowerPoint
1. Click the thumbnail after which the slides should go.
2. **Home › New Slide › Reuse Slides** › *Open a PowerPoint File* › pick a local .pptx. Microsoft says reusing
   slides from cloud files is deprecated; only local files are supported.
3. Tick **Keep source formatting** to keep the original look; leave it clear and the slides take the
   styling of the slide they're inserted after.
4. Click a slide to insert it, or right-click › **Insert All Slides**.
- Inserted slides are copies; editing them doesn't change the original deck.

## Google Slides
**File › Import slides** › choose a presentation from Drive or upload one › select slides (*Select Slides:
All* for everything) › tick *Keep original theme* to import unmodified, or clear it to match this deck ›
**Import slides**. Linked slides: copy slides from another Slides deck, paste, and choose **Link slides**;
an **Update** button then appears when the source changes.

## LibreOffice Impress
**Slide › Insert Slide from File**.

## Gotchas
- Keeping source formatting brings the other deck's design with it, so the deck can end up with mixed
  fonts and masters. Prefer this deck's theme, then fix exceptions.
- Speaker notes come along; check them (PowerPoint's Document Inspector can remove all presentation notes).

## Verify
- [ ] View › Slide Master shows only the masters you meant to have.

## Checked
2026-10-27, against Microsoft Support (Reuse (import) slides from another presentation, PowerPoint for Microsoft 365 and 2016-2024; Document Inspector), Google Workspace presentation tips (Import slides), Google Docs Editors Help (Link a chart, table or slides) and the LibreOffice help master branch (Impress Insert menu). Confirmed: the Reuse Slides path, the Keep source formatting check box (not "Use source formatting"), the deprecation of reusing slides from cloud files, Insert All Slides, the Google Import slides steps and Keep original theme, Link slides and Update, and Impress Insert Slide from File. Removed unconfirmed paste-option keys and a Keynote drag-and-drop claim.
Method: documentation only; no commands were run.
