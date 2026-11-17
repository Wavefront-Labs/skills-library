---
id: computing-software.web-development.web-accessibility.complex-images-and-long-descriptions
name: complex-images-and-long-descriptions
category: computing-software
field: web-development
product: web-accessibility
tags: [text-alternatives, complex-images, long-description, charts, wcag-1-1-1, accessible-charts]
level: practitioner
status: docs-checked
description: "Providing text alternatives for charts, diagrams, maps and infographics: short alt plus long description, data tables, figure and aria-describedby, and accessible SVG charts."
sources:
  - https://www.w3.org/WAI/tutorials/images/complex/
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
  - https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Complex images and long descriptions

## 1. Two-part alternative
1. **Short alt**: identify the image and its key takeaway - `alt="Bar chart: 2026 revenue grew in every region, led by APAC at +34%."`
2. **Long description**: all the information - data values, relationships, process steps - in text that everyone can access.

## 2. Where the long description goes
- **Visible text next to the image** (best - helps everyone): a summary paragraph plus a data table, often in a `<details>`:
```html
<figure aria-labelledby="fig1-cap">
  <img src="revenue.png" alt="Bar chart of 2026 revenue by region; details below.">
  <figcaption id="fig1-cap">Figure 1. Revenue by region, 2026.</figcaption>
  <details><summary>Chart data</summary><table>…</table></details>
</figure>
```
- Separate page linked right after the image ("Text description of the org chart").
- `aria-describedby="desc-id"` pointing to on-page text - assistive technology treats the referenced text as one continuous paragraph (no headings or tables), so use it only for text-only descriptions and prefer visible structured content for long data.
- `longdesc` has inconsistent support (the W3C tutorial notes that Safari and mobile platforms do not support it) - don't rely on it alone.

## 3. Type-specific guidance
- **Charts**: trend + extremes in summary; full data in a table. Whatever charting library is used, still publish the data as a table or text rather than relying only on the library's accessibility features.
- **Diagrams/flowcharts**: describe as a nested list of steps/relationships.
- **Maps**: give the purpose - addresses, directions, regions as text; interactive maps need a list alternative.
- **Infographics**: publish the text content as HTML; the graphic becomes supplementary.

## 4. SVG charts
```html
<svg role="img" aria-labelledby="t d"><title id="t">Revenue by region 2026</title><desc id="d">APAC +34%, EMEA +12%...</desc>…</svg>
```
Or make the SVG `aria-hidden` and provide the data table.

## 5. Colour
Charts must not rely on colour alone (patterns, direct labels) - WCAG 1.4.1 - and need 3:1 contrast for meaningful graphical parts (1.4.11).

## Verify
Hide the image and confirm a user can answer the same questions from the text; screen-reader test that the table is reachable and labelled.

## Checked

- Date: 2026-10-26. Documentation: W3C WAI Images tutorial (complex images), WCAG 2.2 (1.1.1, 1.4.1, 1.4.11).
- Confirmed: short alt plus long description; `figure`/`figcaption` grouping; `aria-describedby` treats the target as one paragraph without structure; `longdesc` support is limited (no Safari or mobile support); SVG `title` referenced through `aria-labelledby`; 1.4.11 Non-text Contrast is AA.
- Removed (no documentation found): the "obsolete-ish" wording and the claims about Highcharts, Chart.js and Vega-Lite features; the vendor link was dropped.
Method: documentation only; no commands were run.