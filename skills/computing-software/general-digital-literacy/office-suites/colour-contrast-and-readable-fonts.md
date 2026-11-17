---
id: computing-software.general-digital-literacy.office-suites.colour-contrast-and-readable-fonts
name: colour-contrast-and-readable-fonts
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, colour-contrast, contrast-ratio, readable-fonts, font-size, colour-blindness, sans-serif, dyslexia-friendly]
level: intro
status: docs-checked
description: "Choose text/background colour contrast of at least 4.5:1, readable font sizes and faces, and avoid colour-only meaning in documents, slides and spreadsheets."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://www.w3.org/WAI/fundamentals/accessibility-intro/
  - https://support.microsoft.com/en-us/accessibility/office-accessibility/rules-for-the-accessibility-checker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Colour contrast and readable fonts

**Goal:** text everyone can read, including people with low vision or colour blindness, on screen or projected.

## Contrast
- WCAG 2.2 success criterion 1.4.3 (AA): **4.5:1** for normal text and **3:1** for large text (18 point, or 14 point bold).
- Black on white is 21:1; grey `#767676` on white is about 4.54:1 (passes), `#777777` is about 4.48:1 (just fails); both computed with the WCAG luminance formula.
- Use a contrast checker for every text and background pair. Office's Accessibility Checker warns about text with insufficient contrast against its background.
- Projectors wash out colours: allow extra contrast and put a solid or semi-transparent box behind text over photos.

## Do not rely on colour alone
Red/green status cells, coloured chart lines and "items in red are mandatory" fail people with colour-vision deficiency. Add text ("Overdue"), symbols, patterns or direct labels.

## Fonts
- Choose plain, clearly shaped typefaces and sizes you can read from the back of the room or at normal screen distance; avoid decorative and condensed faces for body text.
- Left-align body text and avoid long passages of italics, ALL CAPS, or underline that looks like a link.

## Verify
- [ ] Every text/background pair you used passes 4.5:1 (3:1 for large text) in a contrast checker.
- [ ] Print or view in greyscale: all meaning survives.

## Checked

2026-10-27. W3C WCAG 2.2 Understanding 1.4.3 (4.5:1, 3:1 large = 18 pt or 14 pt bold) and Microsoft rules page (contrast is a Warning); contrast ratios of 21:1, #767676 and #777777 computed in Python. Removed: 3:1 for chart elements and icons (that is a different criterion), colour-deficiency prevalence figure, font-size ranges, named typefaces and line-spacing figures (no source), WebAIM tool link.

Method: documentation only; no commands were run.
