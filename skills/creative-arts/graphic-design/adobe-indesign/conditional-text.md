---
id: creative-arts.graphic-design.adobe-indesign.conditional-text
name: conditional-text
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, conditional-text, conditions-panel, condition-sets, document-versions, language-versions, long-documents, versioning]
level: practitioner
status: draft
description: "Produce several versions of an InDesign document from one file with conditional text: conditions, sets, indicators, and what conditions can and cannot hide."
sources:
  - https://helpx.adobe.com/indesign/using/conditional-text.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conditional text for versions

**Goal:** one InDesign file that outputs variants (US/UK spelling, student/teacher edition, Mac/Windows
manual, price lists per region) by showing or hiding tagged text.

## Set up (Window > Type & Tables > Conditional Text)
1. **New Condition** for each variable: name (`UK`, `US`, `Teacher`), indicator method (underline or
   highlight), colour. Indicators are shown on screen, never printed (Show/Hide Indicators: show and print
   indicators only for proofing).
2. Select text, click a condition to apply. Text can have several conditions; it shows if **any** of its
   conditions is visible.
3. Toggle the eye next to each condition to show or hide.
4. **Condition Sets:** save visibility combinations (`UK edition` = UK on, US off, Teacher off) from the
   Set menu; switch the whole document with one click before output.

## What can be conditional
- Text ranges, including anchored objects in the text (an anchored image disappears with its text).
- Not whole frames, page items or pages: use **layers** for those (layer per version) and combine with
  condition sets in a checklist.

## Workflow
- Agree conditions with editors before typesetting. Conditions are applied in InDesign, by hand or via
  GREP Find/Change on tagged markers in the manuscript (e.g. `[[UK]]...[[/UK]]`), then delete the markers.
- Before export: choose the set, update cross-references and TOC, check for overset text (hidden text
  changes the flow), then export with a version-named PDF.

## Gotchas
- Hidden conditional text still exists: Find/Change and spellcheck may skip or include it depending on
  settings; search with conditions visible.
- Text reflow differs per version; check pagination of every version, not just one.
- Index markers and cross-references in hidden text produce odd results; avoid putting them in conditional text.

## Verify
- [ ] Each condition set exported and checked for overset and pagination.
- [ ] Indicators off (or hidden) in final PDFs.
