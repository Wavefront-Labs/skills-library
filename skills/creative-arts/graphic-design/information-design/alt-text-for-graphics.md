---
id: creative-arts.graphic-design.information-design.alt-text-for-graphics
name: alt-text-for-graphics
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, alt-text, long-description, accessible-graphics, image-description, wcag, svg-accessibility]
level: practitioner
status: draft
description: "Write alt text and long descriptions for graphics: decide decorative vs informative, state the point, describe charts with a data table, and markup HTML and SVG correctly."
sources:
  - https://www.w3.org/WAI/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alt text and long descriptions for graphics

**Goal:** people who cannot see a graphic get the same information, by text.

## 1. Decide what the image does (WCAG 1.1.1)
- **Informative:** convey the content and purpose.
- **Decorative:** use empty alt (`alt=""`) in HTML so assistive technology skips it; do not write "decorative" in the text.
- **Functional (a linked or button image):** describe the action ("Download the report (PDF)"), not the picture.
- **Complex (charts, diagrams, maps):** short alt for the identity plus a long description.

## 2. Writing short alt text
- Say what the image shows and why it is there, in context; do not start with "image of".
- Keep it brief, a sentence or two; there is no fixed limit, but very long strings are tiring (125 characters is a widely used rule of thumb).
- Do not repeat the caption word for word; the alt and caption together should add up.
- Include text that appears in the image.

## 3. Charts and complex graphics
1. Short alt: the type and the finding ("Line chart: rents rose faster than wages from 2015 to 2025").
2. Long description: either visible text beside the figure, a linked page, or a data table of the values. A data table covers readers who want exact numbers.
3. Mention trend, extremes and comparisons rather than reading every point.

## 4. Markup
- HTML: `<img alt="...">`; for a long description use adjacent text or `aria-describedby` pointing at it; `<figure>` and `<figcaption>` for captions.
- Inline SVG: add `role="img"` with `<title>` (and `<desc>`) and `aria-labelledby`, or hide decorative SVG with `aria-hidden="true"`.
- In documents (PDF, Word, InDesign export): set alt text in the object properties (InDesign: Object > Object Export Options > Alt Text) and tag PDFs. Check with a screen reader.

## 5. Check
Turn images off and read the page; use a screen reader on the page; ask whether each graphic's message survives in text alone.

## Failure modes
- Alt text that repeats surrounding text.
- Text embedded in an image with no alt.
- Chart described as "bar chart" only.
