---
id: computing-software.software-engineering.code-review.accessibility-focused-review
name: accessibility-focused-review
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, accessibility-review, wcag, a11y, aria, frontend-review]
level: practitioner
status: draft
description: "Review UI changes for accessibility: semantic HTML, keyboard and focus, labels and names, ARIA misuse, contrast and motion, with automated checks and a quick manual pass."
sources: ["https://www.w3.org/WAI/WCAG22/quickref/", "https://www.w3.org/WAI/ARIA/apg/", "https://github.com/dequelabs/axe-core", "https://developer.mozilla.org/en-US/docs/Web/Accessibility"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accessibility-focused review

## Code-level checks (read the diff)
- **Semantic elements**: `<button>` for actions, `<a href>` for navigation, headings in order,
  lists, `<table>` with `<th scope>` for data. A `<div onClick>` is not keyboard- or screen-reader-
  accessible without extra work; ask for a button.
- **Names and labels**: every input has a `<label for>` or `aria-label(ledby)`; icon-only buttons have
  an accessible name; images have meaningful `alt` (or `alt=""` if decorative).
- **ARIA**: first rule of ARIA is don't use it if native HTML does the job. Check roles have the
  required states (`aria-expanded` on disclosure buttons, `aria-selected` on tabs) and keyboard
  behaviour per the ARIA Authoring Practices pattern. Wrong ARIA is worse than none.
- **Focus**: no `outline: none` without a visible replacement (`:focus-visible`); modals trap and
  restore focus; `tabindex` > 0 is a red flag; dynamic content moves focus sensibly.
- **Announcements**: async updates, errors and toasts use live regions (`role="status"`,
  `aria-live="polite"`) or focus management.
- **Forms**: errors associated with fields (`aria-describedby`), not colour-only, required fields
  marked.
- **Colour and motion**: text contrast 4.5:1 (3:1 large text, UI components); respects
  `prefers-reduced-motion`; no information by colour alone.
- **Touch/pointer targets**: at least 24x24 CSS px (WCAG 2.2 2.5.8).
- Mobile native: `contentDescription` (Android), `accessibilityLabel` (iOS/React Native), Dynamic Type.

## Run it (5-minute manual pass)
1. Tab through the changed UI with keyboard only: everything reachable, operable, visible focus,
   logical order, Escape closes dialogs.
2. Zoom to 200% / narrow viewport: no loss of content.
3. Screen reader spot check (VoiceOver, NVDA) on new components.

## Automation
axe-core via `@axe-core/playwright`, jest-axe, Storybook a11y addon, Lighthouse CI, eslint-plugin-
jsx-a11y in lint. Automated tools find roughly a third of issues; they don't replace the manual pass.
