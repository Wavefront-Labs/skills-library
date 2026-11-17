---
id: creative-arts.design-for-form-and-experience.interaction-design.handling-text-truncation-and-overflow
name: handling-text-truncation-and-overflow
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [text-truncation, text-overflow, ellipsis, line-clamp, ui-typography, long-content, internationalization]
level: practitioner
status: draft
description: "Handle text truncation and overflow: when to truncate, wrap or reveal, middle truncation for IDs and filenames, line-clamp, tooltips, and testing with long strings."
sources:
  - "MDN Web Docs - text-overflow and line-clamp (developer.mozilla.org/docs/Web/CSS/text-overflow)"
  - "Material Design 3 - Text fields and lists, text overflow behaviour (m3.material.io)"
  - "Nielsen Norman Group - Truncation and Show More (nngroup.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text truncation and overflow

**Goal:** layouts survive long, short and translated text without hiding what users need.

## Decide: wrap, truncate or reveal
- **Wrap** (default) for content users must read: names, descriptions, labels in forms. Let containers grow.
- **Truncate** where space is fixed and the full text is available elsewhere: list titles, table cells, chips, breadcrumbs.
- **Reveal:** "Show more" for long descriptions; tooltip or detail view for truncated items (not tooltips alone, since touch has no hover).
- Never truncate: error messages, prices, dates, key labels, instructions.

## CSS patterns
```css
.one { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
.clamp { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
```
- In flex or grid children set `min-width: 0` or the ellipsis never triggers.
- **Middle truncation** for filenames and IDs (keep the extension or suffix): done in JS or as two spans (`report-final-v...2.pdf`).
- Truncate numbers never; shrink via layout (abbreviate 1.2k with a title attribute).

## Test with hostile strings
- Very long single words with no spaces; 50-100 character names; German (+30 percent), Finnish; right-to-left (Arabic, Hebrew); empty strings; emoji.
- Use real content or a plugin (Figma Content Reel, "Lorem ipsum" long variants) before sign-off.
- Provide accessible full text (title attr is weak; use aria-label or visible expansion).

## Verify
- [ ] Each text slot decided: wrap, truncate or reveal.
- [ ] Flex/grid children have `min-width: 0`.
- [ ] Tested with long, short and RTL strings.
