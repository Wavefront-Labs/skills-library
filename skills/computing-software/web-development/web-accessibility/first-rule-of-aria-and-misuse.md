---
id: computing-software.web-development.web-accessibility.first-rule-of-aria-and-misuse
name: first-rule-of-aria-and-misuse
category: computing-software
field: web-development
product: web-accessibility
tags: [name-role-value, wcag-robust, first-rule-of-aria, aria-misuse, redundant-roles, aria-hidden-focusable, role-presentation, no-aria-better-than-bad-aria]
level: practitioner
status: verified
description: "Avoiding ARIA misuse: native HTML first, redundant or conflicting roles, aria-hidden on focusable content, presentation roles stripping semantics, and audits."
sources:
  - https://www.w3.org/TR/using-aria/
  - https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
  - https://webaim.org/projects/million/
  - https://www.w3.org/TR/html-aria/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First rule of ARIA and common misuse

**Goal:** ARIA only where HTML can't express the semantics - because wrong ARIA is worse than none (WebAIM Million 2026: home pages with ARIA averaged 59.1 detected errors against 42 without; correlation, not proof that ARIA caused them).

## 1. The rules of ARIA use (W3C "Using ARIA")
Using ARIA (now a W3C discontinued draft, 24 Feb 2026) has four rules:
1. Use a native element if one exists (`<button>`, not `<div role="button">`).
2. Don't change native semantics unless you must (the document's example: not `<h2 role="tab">` but `<div role="tab"><h2>heading tab</h2></div>`).
3. All interactive ARIA controls must be keyboard operable.
4. Don't use `role="presentation"`/`aria-hidden="true"` on a focusable element (an aria-hidden ancestor counts too).

Separately, WCAG 4.1.2 requires every interactive element to have an accessible name. Run in Chromium: `<button role=presentation>` is still exposed as a button.

## 2. Misuse catalogue
| Misuse | Problem | Fix |
|---|---|---|
| `<div role="button" onclick>` | No focus, no Enter/Space | `<button type="button">` |
| `<button role="button">`, `<nav role="navigation">`, `<ul role="list">`* | Redundant noise | Remove (*except: Safari/VoiceOver drops list semantics when list styles are removed, except inside `<nav>` (Scott O'Hara, 2019); `role="list"` is the deliberate workaround; Chromium keeps the list, run) |
| `aria-hidden="true"` on an element containing links/buttons | Focusable but invisible to AT ("ghost" focus) | Use `inert` or `hidden`, or remove from tab order |
| `role="presentation"` on `<table>` with data | Strips table semantics | Only for layout tables |
| `aria-label` on `<div>`/`<span>` with no role | ARIA 1.2 prohibits naming a generic element and AT support is inconsistent (Chromium still exposes the name, run) | Give it a role or use visible text |
| `role="menu"` for site navigation | Promises app-menu keyboard model (arrows) users then don't get | `<nav>` + list of links |
| `aria-live` on a large region | Constant chatter | Small dedicated status region |
| `role="application"` | Turns off screen reader browse mode | Almost never |
| `tabindex="0"` on non-interactive text "for screen readers" | Extra tab stops; SR users don't need it | Remove |

## 3. Audit approach
- axe-core rules: `aria-allowed-role`, `aria-hidden-focus`, `aria-prohibited-attr`, `nested-interactive`, `aria-required-children`.
- Lint: `eslint-plugin-jsx-a11y`, `eslint-plugin-vuejs-accessibility`, `@angular-eslint/template/accessibility`.
- Check the ARIA in HTML spec (html-aria) for allowed roles per element.

## Verify
- [ ] axe reports zero ARIA rule violations.
- [ ] Every `role=` in the codebase justified (grep and review).
- [ ] No focusable element inside `aria-hidden` (axe `aria-hidden-focus`).
