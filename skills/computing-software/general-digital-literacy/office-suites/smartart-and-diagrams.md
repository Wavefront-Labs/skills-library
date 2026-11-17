---
id: computing-software.general-digital-literacy.office-suites.smartart-and-diagrams
name: smartart-and-diagrams
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slide-content, smartart, diagrams, process-diagram, org-chart, convert-to-smartart, google-slides-diagram]
level: intro
status: docs-checked
description: "Turn bullet lists into SmartArt process, cycle, hierarchy and org-chart diagrams in PowerPoint, and build simple diagrams in Google Slides and Impress."
sources:
  - https://support.microsoft.com/en-us/office/add-smartart-to-a-slide-1f033051-901b-44ae-a9f5-4d23996679c8
  - https://support.microsoft.com/en-us/office/graphics-visuals/learn-more-about-smartart-graphics
  - https://support.microsoft.com/en-us/powerpoint/convert-your-smartart-graphic-into-shapes
  - https://support.google.com/docs/answer/1696521
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/orgchart.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/04/01020000.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SmartArt and diagrams

**Goal:** show a process, hierarchy or cycle visually instead of as a bullet list.

## PowerPoint SmartArt
- Insert › **SmartArt** › pick from the gallery's types: List, **Process**, **Cycle**, **Hierarchy** (org charts),
  Relationship, Matrix, Pyramid, Picture and more.
- Faster: select the bulleted text › Home › **Convert to SmartArt Graphic** › pick a layout.
- Type in the **Text pane**, which works like an outline: each bullet becomes a shape or a bullet inside a
  shape, depending on the layout. Some fixed-shape layouts show only part of the text.
- To tweak shapes by hand: SmartArt Design › Reset group › **Convert › Convert to Shapes**. This is one-way;
  the shapes can't be turned back into SmartArt.

## Google Slides
Insert › **Diagram** › choose a style, number of levels and template, then edit the text. Use Insert › Shape
and Line for anything else.

## LibreOffice Impress
Draw shapes from the Flowchart toolbar and join them with **connectors** from the Connectors toolbar (they
attach to the shapes' connection sites); group with `Ctrl+Shift+G`.

## Gotchas
- Keep text to a few words per shape; long text shrinks and becomes hard to read.
- Many shapes on one slide: split across two slides or use a simpler layout.

## Verify
- [ ] The diagram reads correctly left-to-right/top-down and all text is legible from the back row.

## Checked
2026-10-27, against Microsoft Support (Create a SmartArt graphic from a list; Learn more about SmartArt graphics; Convert your SmartArt graphic into shapes; PowerPoint for Microsoft 365 and 2016-2024), Google Docs Editors Help (shapes and diagrams) and the LibreOffice help master branch (Impress flowchart guide; shortcut keys). Confirmed: SmartArt types, Convert to SmartArt Graphic, Text pane behaviour, Convert to Shapes and that it is one-way, Google Insert › Diagram options, Impress connectors and group shortcut. Removed unconfirmed Text pane keys, a convert-to-text path, Google diagram style names, an elbow-connector path, a shape-count limit and a screen-reader claim.
Method: documentation only; no commands were run.
