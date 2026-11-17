---
id: creative-arts.graphic-design.typography.text-contrast-and-minimum-sizes
name: text-contrast-and-minimum-sizes
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, screen-typography, text-contrast, wcag, contrast-ratio, large-text, accessibility, legibility, minimum-type-size, apca, low-vision]
level: practitioner
status: docs-checked
description: "Make text readable for everyone: WCAG 2.2 contrast ratios (4.5:1, 3:1 large text), what counts as large, practical minimum sizes, and how to test."
sources:
  - https://www.w3.org/TR/WCAG22/#contrast-minimum
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://webaim.org/resources/contrastchecker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text contrast and minimum sizes

**Goal:** text that passes accessibility requirements and stays readable for people with low vision, on
real screens and real paper.

## WCAG 2.2 contrast requirements
| Criterion | Normal text | Large text |
|---|---|---|
| 1.4.3 Contrast (Minimum), AA | **4.5:1** | **3:1** |
| 1.4.6 Contrast (Enhanced), AAA | 7:1 | 4.5:1 |
- **Large text** = at least **18 pt** regular, or **14 pt (about 18.66 px) bold**.
- Ratio = (L1 + 0.05) / (L2 + 0.05) using relative luminance. Check any pair with a contrast checker.
- Exemptions: logos and brand names, purely decorative text, inactive UI controls. Text over images still
  needs contrast: add a scrim or overlay.

## Minimum sizes (practice, not WCAG rules)
WCAG sets no minimum point size, only the large-text threshold above. Legal and pharmaceutical print minimums
vary by jurisdiction: check the regulation.
- Very light weights at small sizes can fail visually even when the colour ratio passes.

## Testing
- Pick colours with a checker: WebAIM Contrast Checker or a similar tool.
- Text over images: sample the lightest area behind the text.
- WCAG 2.2 ratios remain the reference; APCA is an alternative model, a second opinion only.
- Print: check in daylight-balanced light; uncoated paper lowers contrast (ink spreads, paper is greyer).

## Gotchas
- Brand colours often fail for body text; define accessible text variants of brand colours.
- Placeholder text and disabled states are the most common failures.
- Thin fonts rendered on Windows look lighter than in design tools on Retina screens.

## Checked
2026-11-01. Confirmed against the WCAG 2.2 Understanding Contrast (Minimum) page and the WebAIM Contrast Checker
page: 4.5:1 normal and 3:1 large text, 7:1 enhanced, large text as 18 point or 14 point bold (18.66 px), exemptions
for decorative text, inactive controls and logotypes. Removed unconfirmed screen and print size figures, the EU
labelling figure and the grey hex example.
Method: documentation only; no commands were run.

## Verify
- [ ] Every text/background pair is listed with its ratio and passes AA.
- [ ] Smallest text size in the spec is stated and tested on target devices or paper.
