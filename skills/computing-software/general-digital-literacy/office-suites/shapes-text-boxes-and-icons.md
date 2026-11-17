---
id: computing-software.general-digital-literacy.office-suites.shapes-text-boxes-and-icons
name: shapes-text-boxes-and-icons
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, shapes-and-text-boxes, text-box, icons, ms-word, google-docs, drawing]
level: intro
status: draft
description: "Insert, size, align and group shapes, text boxes and icons in Word, Google Docs and LibreOffice Writer without breaking the page layout."
sources:
  - https://support.microsoft.com/en-us/word
  - https://support.google.com/docs
  - https://help.libreoffice.org/latest/en-US/text/shared/main0000.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shapes, text boxes and icons

**Goal:** a callout, label or simple diagram that stays where you put it when the text around it changes.

## Word
- **Insert › Shapes** › pick one › drag on the page. Hold `Shift` while dragging for a perfect circle/square or a straight line.
- **Insert › Text Box › Draw Text Box** for a free-floating label; or right-click any shape › **Add Text**.
- **Insert › Icons** (Microsoft 365) for single-colour SVG icons; recolour with **Graphics Format › Graphics Fill**.
- Layout: the **Layout Options** button beside the object › *In Line with Text* (moves like a character) or *Square / In Front of Text* (floats). Floating objects are anchored to a paragraph (anchor icon); tick **Move object with text** so they follow it, or **Fix position on page** for letterhead-style items.
- Several objects: `Ctrl`+click each › **Shape Format › Group** so they move as one; **Align › Align Center / Distribute Horizontally** to line them up.
- **Selection Pane** (Home › Select › Selection Pane) lists every object: pick hidden ones, rename, show/hide.

## Google Docs
- **Insert › Drawing › + New**: shapes, arrows, text boxes on a canvas › **Save and close**. Click the drawing › **Edit** to change it later.
- Wrap options under the image: *In line*, *Wrap text*, *Break text*, *Behind/In front of text*.
- Icons: Insert › Image › Search the web is gone; use Drawing shapes or upload an SVG/PNG exported from an icon set with a free licence.

## LibreOffice Writer
Show the **Drawing** toolbar (View › Toolbars › Drawing). Right-click › **Anchor** › *To Paragraph / To Character / As Character*; **Wrap** sets text flow. Group with `Ctrl+Shift+G`.

## Gotchas
- Text in text boxes is skipped by many screen readers and by some find/replace and word counts; keep essential content in the main text.
- Shapes drawn "on top" of an in-line picture drift when text reflows; group them with the picture or put both in a drawing canvas (Insert › Shapes › New Drawing Canvas).
- Exporting to PDF keeps shapes; converting Word ↔ Google Docs often flattens or drops grouped drawings.

## Verify
- [ ] Add a paragraph above the object: it moves as intended (with its paragraph, or stays fixed).
- [ ] The Selection Pane shows each object with a meaningful name.
