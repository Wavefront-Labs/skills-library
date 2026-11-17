---
id: creative-arts.graphic-design.typography.optical-margin-alignment-and-hanging-punctuation
name: optical-margin-alignment-and-hanging-punctuation
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, justification, text-alignment, optical-margin-alignment, hanging-punctuation, story-panel, hanging-quotes, hanging-bullets, css-hanging-punctuation, optical-alignment]
level: practitioner
status: draft
description: "Make text edges look straight by hanging punctuation and serifs slightly outside the measure: InDesign Optical Margin Alignment, manual hanging quotes and bullets, and CSS options."
sources:
  - https://helpx.adobe.com/indesign/using/formatting-paragraphs.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Optical margin alignment and hanging punctuation

**Goal:** text edges that look straight to the eye, not just mathematically aligned.

## The problem
Quotes, hyphens, commas, full stops and the diagonal strokes of A, V, W, T leave a visible notch at the left or
right edge of a column when aligned exactly to the frame edge. Large display quotes make it obvious.

## InDesign: Optical Margin Alignment
- Window > Type & Tables > **Story** panel > **Optical Margin Alignment** on, size field = the text size (e.g. 10 pt).
  It applies to the whole story.
- Punctuation hangs fully, letters like A, T, V, W hang slightly, both sides.
- Exclude a paragraph (e.g. a bulleted list or tabular text) with the paragraph style option **Ignore Optical Margin**
  (Indents and Spacing).

## Manual hanging (headlines, pull quotes, display)
- **Opening quote:** move it outside the text edge: set left indent 0 and use a negative first-line indent equal to
  the quote's width, or kern/track it out; in Illustrator, use Optical Margin Alignment (Type > Optical Margin
  Alignment) or a separate frame for the quote.
- **Bullets:** hang bullets into the margin so text aligns with the body edge (see bullets skill), a common
  editorial preference.
- Drop caps with a quote: hang the quote mark outside.

## Web (CSS)
- `hanging-punctuation: first allow-end;` hangs opening quotes and end punctuation - **supported in Safari only**
  at time of writing. Fallback: a negative `text-indent` on blockquotes that start with a quote mark
  (e.g. `text-indent: -0.45em;`), scoped with a class.

## Gotchas
- Optical alignment changes line lengths slightly and can reflow text - turn it on before final proofing.
- With very tight gutters, hanging punctuation can look like it intrudes on the next column; keep gutters adequate.
- Do not use it for tabular or code text where exact alignment matters.

## Verify
- [ ] Quotes and hyphens at column edges no longer create visible indents.
- [ ] Lists and tables excluded where alignment must be exact.
