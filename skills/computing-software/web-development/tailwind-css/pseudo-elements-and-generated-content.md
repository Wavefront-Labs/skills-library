---
id: computing-software.web-development.tailwind-css.pseudo-elements-and-generated-content
name: pseudo-elements-and-generated-content
category: computing-software
field: web-development
product: tailwind-css
tags: [css-selectors, pseudo-classes, pseudo-elements, before-after, marker, backdrop, placeholder, selection, first-letter, generated-content]
level: practitioner
status: docs-checked
description: "Using pseudo-elements (::before/::after, ::marker, ::backdrop, ::placeholder, ::selection, ::file-selector-button) correctly, including accessibility of generated content."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements
  - https://developer.mozilla.org/en-US/docs/Web/CSS/content
  - https://developer.mozilla.org/en-US/docs/Web/CSS/::backdrop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pseudo-elements and generated content

**Goal:** decorate and style parts of elements without extra markup, and without hiding meaning from assistive tech.

## 1. ::before / ::after
```css
.badge::before { content: ""; inline-size: .5em; block-size: .5em; border-radius: 50%; background: currentColor; display: inline-block; }
.external::after { content: " ↗" / ""; }          /* alt text after the slash */
.required::after { content: " *" / " required"; }   /* alt text for speech output */
```
- For `::before` and `::after`, `content` computes to `none` by default, so the pseudo-element does not render until you set it (even `""`).
- `content` accepts alternative text after a `/`, intended for speech output by screen readers (some browsers may also display it). Never put essential information only in `content`.

## 2. Useful others
| Pseudo-element | Use |
|---|---|
| `::marker` | List bullets/numbers on `display: list-item` boxes (`li`, `summary`): `li::marker { color: var(--brand); content: "→ "; }`. Only a limited set of properties applies (font, `color`, `content`, counters, `white-space` and a few more). |
| `::backdrop` | Box the size of the viewport beneath a top-layer element: modal `<dialog>` (via `showModal()`), fullscreen, popover. `dialog::backdrop { background: rgb(0 0 0 / .5); }` |
| `::placeholder` | Placeholder text - keep enough contrast if it conveys info |
| `::selection` | Highlight colours; keep contrast |
| `::file-selector-button` | Style the button of `<input type=file>` |
| `::first-letter`, `::first-line` | Typographic drop caps |
| `::part()`, `::slotted()` | Shadow DOM (see web components skills) |
| `::view-transition` | View transition pseudo-elements |
| `::details-content` | The expandable/collapsible contents of a `<details>` element |

## 3. Gotchas
- Pseudo-elements use a double colon; browsers support the single-colon syntax only for the original four (`::before`, `::after`, `::first-line`, `::first-letter`).
- A pseudo-element must come after all other components of the selector; the last element in the selector is its originating element, so `p::first-line > *` is invalid.
- `::backdrop` neither inherits from nor is inherited by any other element, so custom properties set on the `dialog` do not reach it; define them on `::backdrop` or `:root`.

## Verify
- [ ] Screen reader doesn't announce decorative generated content; does announce meaningful ones.
- [ ] Modal backdrop styled in all target browsers.

## Checked
2026-11-01. Confirmed on MDN (pseudo-elements, content, ::backdrop, ::marker, ::details-content): double-colon rule and legacy single-colon four, originating-element rule, content default and alt-text syntax, ::marker allowed properties, ::backdrop scope and non-inheritance, ::details-content. Removed: void-element claim, screen-reader exposure claim, contrast ratio figure, backdrop-filter, JS/event claim, empty-alt-is-decorative claim.
Method: documentation only; no commands were run.
- [ ] Placeholder and selection colours meet contrast.
