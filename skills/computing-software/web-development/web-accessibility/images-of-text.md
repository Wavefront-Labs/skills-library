---
id: computing-software.web-development.web-accessibility.images-of-text
name: images-of-text
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, images-of-text, wcag-1-4-5, typography, web-fonts]
level: practitioner
status: docs-checked
description: "Meeting WCAG 1.4.5 Images of Text: using real styled text instead of text baked into images, the logo and essential exceptions, and fixing banners, buttons and social graphics."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html
  - https://www.w3.org/WAI/WCAG22/Techniques/css/C22
  - https://www.w3.org/WAI/WCAG22/Techniques/general/G140
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Images of text

**1.4.5 (AA):** if the technologies can achieve the visual presentation, use text rather than images of text. Exceptions: customisable images of text (user can customise it visually) and **essential** presentation (logotypes are named in the SC as essential). AAA (1.4.9, Images of Text (No Exception)) allows only pure decoration or essential text.

## 1. Why
Images of text don't reflow, pixelate when zoomed, ignore user font/colour/spacing overrides (1.4.12, high contrast), aren't translatable, and need alt text that's often missing or stale.

## 2. Typical offenders and fixes
| Offender | Fix |
|---|---|
| Hero banners with headline and CTA baked into a JPEG | HTML heading + button over a background image (scrim for contrast) |
| Promotional tiles/carousels from marketing tools | Template with live text fields; let marketers fill text, not upload flattened images |
| Buttons/nav as images | CSS-styled `<button>`/links with web fonts |
| Quotes/testimonials as graphics | `<blockquote>` with styling |
| Tables or code screenshots in docs | real `<table>` / `<pre><code>` |
| Fancy headings in a brand font | web font via `@font-face` (WOFF2, `font-display: swap`) |
| Infographic text | HTML text alternative next to it |

## 3. Allowed
Logos (including text in the logo) and pictures that contain significant other visual content, such as graphs, screenshots and diagrams, which the Understanding page does not treat as plain images of text. Still give appropriate alt text.

## 4. CMS governance
Restrict image upload fields for areas meant to hold copy; provide text-overlay components.

## Verify
Zoom in and switch to forced colors: real text adapts, images of text don't - inventory and replace remaining ones.

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text: 1.4.5 Images of Text is Level AA with the customizable and essential exceptions (logotypes essential); 1.4.9 is Level AAA and allows only pure decoration or essential presentation. The Understanding page treats pictures with significant other visual content (graphs, screenshots, diagrams) separately. MDN confirms the font-display swap value. Removed the typeface-specimen, screenshot and social-image claims and the 400% figure.

Method: documentation only; no commands were run.
