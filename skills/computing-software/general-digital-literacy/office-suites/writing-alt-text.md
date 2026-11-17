---
id: computing-software.general-digital-literacy.office-suites.writing-alt-text
name: writing-alt-text
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, alt-text, alternative-text, image-descriptions, decorative-images, screen-reader, charts-alt-text]
level: intro
status: docs-checked
description: "Write useful alt text for images, charts and icons in documents and slides, mark decorative images, and know when body text or a data table is better."
sources:
  - https://support.microsoft.com/en-us/accessibility/office-accessibility/add-alternative-text-to-a-shape-picture-chart-smartart-graphic-or-other-object
  - https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities
  - https://support.google.com/docs/answer/179738
  - https://www.w3.org/WAI/tutorials/images/decision-tree/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing alt text

**Goal:** someone who cannot see the image gets the same information from its description.

## Add it
- Microsoft 365: right-click the object and choose **View Alt Text** or **Edit Alt Text**, or use the Format tab > **Alt Text**. Give a one- or two-sentence description in the Description box (the Title box is optional, for long explanations). Tick **Mark as decorative** for decorative images; this greys out the text field.
- Automatic alt text can be generated for photos, stock images and icons; check and rewrite it. Charts, SmartArt, screenshots and shapes need alt text added manually.
- Click the outer border of a chart or SmartArt graphic, not a piece inside it.
- Google Docs/Slides: the Alt text command, shortcut **Ctrl+Alt+Y**.

## What to write
1. Ask why the image is there and describe that, briefly.
2. Do not start with "image of" or "picture of".
3. If the image contains text, include the text.
4. Charts: state the takeaway and put the data in a table or the body text.
5. Images that are links: describe the destination.
6. Purely decorative images (borders, background swirls): mark them decorative so they are skipped (W3C image decision tree).

## Examples
- Weak: "graph". Better: "Bar chart showing most customers chose next-day delivery over standard delivery and click and collect."
- Weak: "team photo". Better: "The support team standing in front of the new office."

## Verify
- [ ] Read the document with images hidden (or with a screen reader): nothing important is lost.

## Checked

2026-10-27. Microsoft Support alt-text page and PowerPoint accessibility page (read 2026-10-27), Google Docs keyboard shortcuts (Ctrl+Alt+Y), W3C images decision tree (decorative images). Confirmed menu paths, Description/Title boxes, Mark as decorative, automatic alt text scope, chart/SmartArt handling, avoid 'an image of'. Removed: LibreOffice path, 125-character guide and numeric example data (no source).

Method: documentation only; no commands were run.
