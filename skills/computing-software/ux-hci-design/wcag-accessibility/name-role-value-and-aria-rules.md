---
id: computing-software.ux-hci-design.wcag-accessibility.name-role-value-and-aria-rules
name: name-role-value-and-aria-rules
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [name-role-value, aria-first-rule, wcag-robust-aria]
level: practitioner
status: docs-checked
description: "Expose name, role, state and value for custom widgets and follow ARIA usage rules."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://www.w3.org/TR/using-aria/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name, Role, Value (SC 4.1.2, A)
- SC 4.1.2 (Level A): user interface components programmatically convey their accessible name, role, and current state and value.
- The four rules of ARIA use come from Using ARIA, which is now a Discontinued Draft kept for reference; for current guidance see the ARIA Authoring Practices Guide:
1. If a native HTML element or attribute already has the semantics and behaviour you need, use it instead of adding an ARIA role, state or property.
2. Do not change native semantics unless you really have to (use `<div role=tab><h2>heading tab</h2></div>`, not `<h2 role=tab>`).
3. All interactive ARIA controls must be usable with the keyboard; a `role=button` element must take focus and activate with both Enter and Space.
4. Do not use `role="presentation"` or `aria-hidden="true"` on a focusable element; `aria-hidden` on an ancestor also hides a visible interactive element inside it.
- Accessible name techniques for 4.1.2: `aria-label` where a visible label cannot be used (ARIA14) and `aria-labelledby` for user interface controls (ARIA16).
- Failure: a control with visible label text but no accessible name.

## Verify
- [ ] Custom widgets expose correct role, name and state in the accessibility tree.

## Checked

- Date: 2026-11-09.
- Read Using ARIA (W3C Discontinued Draft, 24 February 2026) in full: the four rules, examples and notes. Searched Understanding SC 4.1.2 Name, Role, Value (Level A) for the criterion wording, ARIA14, ARIA16 and the failure.
- Removed: the fifth "rule" (not in Using ARIA), "no ARIA is better than bad ARIA", the `aria-label` translation and `div`/`span` claims, and the DevTools line (not on the cited pages).

Method: documentation only; no commands were run.
