---
id: creative-arts.design-for-form-and-experience.interaction-design.setting-line-length-for-readable-ui-text
name: setting-line-length-for-readable-ui-text
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [line-length, ui-typography, readability, measure, line-height, typography, text-layout]
level: practitioner
status: docs-checked
description: "Set readable line length and spacing in UI against WCAG 2.2: width limit, line height, text spacing override, reflow and zoom, with max-width in ch units."
sources:
  - "https://www.w3.org/TR/WCAG22/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line length and readability

**Goal:** body text that is comfortable to read at every width.

## What WCAG 2.2 says
- **SC 1.4.8 Visual Presentation (AAA):** a mechanism lets users get a text width of no more than 80 characters (40 if CJK), unjustified text, line spacing of at least 1.5 within paragraphs and paragraph spacing at least 1.5 times the line spacing, and 200 percent resize without horizontal scrolling.
- **SC 1.4.12 Text Spacing (AA):** nothing is lost when users set line height to 1.5 times the font size, paragraph spacing to 2 times, letter spacing to 0.12 times and word spacing to 0.16 times. The criterion is about surviving the override, not about authoring those values.
- **SC 1.4.10 Reflow (AA):** no two-dimensional scrolling at 320 CSS pixels wide (equal to 400 percent zoom of a 1280 pixel viewport), except for content needing two-dimensional layout.

## Practice
- Keep the measure at or below 80 characters; many designers aim for roughly 45-75, which is a convention, not a standard.
- Body line height of about 1.5 is a safe default; shorter lines can take less, longer lines need more.
- Left-align text for left-to-right languages; avoid justified text.

## Implementing
```css
.prose { max-width: 66ch; line-height: 1.5; }
.prose p { margin-block: 1em; }
```
- Use `ch` or `rem`, not px, so it scales with the font.
- Wide screens: keep the text column at its max-width and use side space for secondary content, not longer lines.
- Tables, code and captions can have different measures; do not force them to the prose width.

## Check
- Count characters on a few lines; test on a 320 px phone and a very wide display.
- Zoom to 400 percent: no horizontal scroll for text blocks.
- Apply the SC 1.4.12 spacing values with a bookmarklet or user stylesheet: no clipped or overlapping text.

## Verify
- [ ] Prose max-width set in ch, no more than 80 characters.
- [ ] Line height about 1.5; paragraph spacing set.
- [ ] No horizontal scroll at 400 percent zoom.

## Checked
2026-11-01. Confirmed in WCAG 2.2 (w3.org/TR/WCAG22): the values and levels of SC 1.4.8, 1.4.10 and 1.4.12. Corrected: paragraph spacing in 1.4.12 is 2 times the font size (not 1.5), and reflow is tested at 400 percent zoom (not 200). Removed: the Bringhurst "ideal 66" and Baymard figures and the 40-60 mobile and 90-character claims (sources not read); 45-75 is kept only as a labelled convention.
Method: documentation only; no commands were run.
