---
id: computing-software.web-development.web-accessibility.link-purpose-and-link-text
name: link-purpose-and-link-text
category: computing-software
field: web-development
product: web-accessibility
tags: [navigable, wcag-navigable, link-purpose, link-text, wcag-2-4-4, read-more-links, aria-label-links, card-links]
level: practitioner
status: docs-checked
description: "Writing link text that makes sense out of context (WCAG 2.4.4): fixing 'read more' links, accessible card links, new-window and file-type indicators."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html
  - https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA8
  - https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
  - https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
  - https://inclusive-components.design/cards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Link purpose and link text

**Goal:** screen reader users browsing a links list (and everyone scanning) can tell where each link goes.

## 1. Write it in the text
- Bad: "Click here", "Read more", "Learn more", "More" x 12, raw URLs.
- Good: "Read the 2026 pricing changes", "Download annual report (PDF, 2 MB)".
WCAG 2.4.4 (A) allows purpose from context (same sentence/paragraph/list item/table cell); 2.4.9 (AAA) requires link text alone. Aim for text alone.

## 2. When design insists on "Read more"
```html
<a href="/posts/42">Read more<span class="visually-hidden"> about accessible carousels</span></a>
<!-- or -->
<a href="/posts/42" aria-describedby="post-42-title">Read more</a>
```
Keep the visible text at the **start** of the accessible name (2.5.3 Label in Name - voice users say "click Read more"). Avoid `aria-label` that replaces visible text with different words.

## 3. Card links
Wrapping a whole card in `<a>` makes screen readers read the entire card as the link name. Better: make the heading the link and extend its hit area:
```css
.card { position: relative; }
.card h3 a::after { content: ""; position: absolute; inset: 0; }
```
Other interactive elements in the card need `position: relative; z-index: 1`.

## 4. Indicators
- Opens in new tab: avoid; if needed add "(opens in new tab)" (visible or hidden text) and an icon with alt text.
- File links: type and size in text.
- Links vs buttons: links navigate (`<a href>`), buttons act (`<button>`). An `<a>` without `href` isn't focusable and isn't a link.

## 5. Links distinguishable
Links in body text need more than colour alone: a non-colour cue such as an underline, or at least 3:1 contrast with the surrounding text (1.4.1; see its Understanding page for the conditions).

## Verify
- [ ] Screen reader links list (for example the NVDA elements list or the VoiceOver rotor) - every link understandable alone; no duplicates pointing to different places.
- [ ] Voice control: "click read more" still works where visible text is "Read more".
- [ ] axe: no empty links, no `<a>` without href acting as buttons.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 (2.4.4, 2.4.9, 2.5.3, 1.4.1) and technique ARIA8.
- Confirmed: 2.4.4 is Level A and lets purpose come from the same sentence, paragraph, list item or table cell; 2.4.9 Link Purpose (Link Only) is AAA; 2.5.3 Label in Name is Level A and the Understanding example has the accessible name starting with the visible label; 3:1 contrast between link and surrounding text appears in the 1.4.1 Understanding page.
- Removed (no documentation found): the hover/focus cue requirement and the NVDA key shortcut. The inclusive-components card article was not re-read.
Method: documentation only; no commands were run.