---
id: computing-software.general-digital-literacy.office-suites.handouts-and-exporting-slides
name: handouts-and-exporting-slides
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slideshow, handouts, export-pdf, export-video, print-handouts, notes-pages, create-video]
level: intro
status: docs-checked
description: "Print handouts and notes pages, export a deck to PDF, images or MP4 video, and send slides in a format recipients can open."
sources:
  - https://support.microsoft.com/en-us/powerpoint/print-slides-with-or-without-speaker-notes
  - https://support.microsoft.com/en-us/powerpoint/training/save-powerpoint-presentations-as-pdf-files
  - https://support.microsoft.com/en-us/powerpoint/save-a-slide-as-an-image-or-as-a-separate-presentation-file
  - https://support.microsoft.com/en-us/powerpoint/turn-your-presentation-into-a-video
  - https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks
  - https://support.google.com/docs/answer/143346
  - https://support.google.com/docs/answer/1696787
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/printing.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/shared/00/00000401.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handouts and exporting slides

**Goal:** give the audience something useful afterwards, in a format they can open.

## Print handouts
- **PowerPoint:** File › Print › the second Settings box (*Full Page Slides*) › **Handouts** (several
  slides per page) or **Notes Pages** (one slide per page with your notes below). Only Notes Pages
  prints speaker notes.
- **Google Slides:** File › **Print settings and preview** › *1 slide with notes* or *Handout*.
- **Impress:** File › Print › General tab › Document: **Handouts** or **Notes**, then slides per page.

## Export
| Need | PowerPoint (Windows) | Google Slides |
|---|---|---|
| PDF | File › Export › **Create PDF/XPS Document** (Options › *Publish what*: handouts, outline) | From the slideshow toolbar: download as PDF |
| Video | File › Export › **Create a Video**: Ultra HD (4K), Full HD (1080p), HD (720p) or Standard (480p); uses recorded timings and narration; saves .mp4 or .wmv | not covered here |
| Images | File › Export › JPEG/PNG › *Save Every Slide* or *Save Current Slide Only* | not covered here |
| Editable | .pptx | From the slideshow toolbar: download as PPTX |

Impress: File › Export As › **Export as PDF**; File › Export for other formats. PowerPoint for Mac's
PDF export does not include notes or handouts.

## Which to send
PDF for "read later". PPTX only if they must edit or present it. A video for self-paced viewing
with narration.

## Gotchas
- Images exported from slides drop transitions, animations, video and audio; slides built up by
  animation show everything at once.
- Remove speaker notes and comments before sending the PPTX (File › Info › Check for Issues ›
  Inspect Document).
- Video creation can take a long time for a long deck; start it well before you need it.

## Verify
- [ ] Open the exported PDF/video yourself before sending.

## Checked
2026-10-27, against Microsoft Support (PowerPoint for Microsoft 365 and 2016-2024: print with notes, save as PDF, save slides as images, turn a presentation into a video, Document Inspector), Google Docs Editors Help (Print a file; Present slides) and the LibreOffice help master branch (Impress printing guide, File menu). Confirmed: Handouts and Notes Pages print layouts, Google Print settings and preview options, Impress Document list, Create PDF/XPS Document and its Publish what options, Mac PDF limits, image export options and what they drop, Create a Video quality list and .mp4/.wmv output, Google slideshow download as PDF/PPTX, and Impress Export as PDF. Removed unconfirmed claims about a "lines for notes" layout, grayscale and Google image downloads.
Method: documentation only; no commands were run.
