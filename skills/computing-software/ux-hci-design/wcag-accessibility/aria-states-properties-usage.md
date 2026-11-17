---
id: computing-software.ux-hci-design.wcag-accessibility.aria-states-properties-usage
name: aria-states-properties-usage
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [aria-expanded, aria-labelledby]
level: practitioner
status: docs-checked
description: "Apply aria-expanded, aria-controls, aria-labelledby, aria-describedby, aria-current, aria-hidden and aria-disabled as WAI-ARIA 1.2 defines them."
sources:
  - https://www.w3.org/TR/wai-aria-1.2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Commonly used states and properties (WAI-ARIA 1.2)
- `aria-expanded="true|false"`: whether a grouping element owned or controlled by this element is expanded or collapsed (the toggle control of a disclosure, accordion or menu button).
- `aria-controls`: ID reference list of element(s) whose contents or presence this element controls, for example a tab and its tab panel.
- `aria-labelledby`: ID reference(s) of the element(s) that label this element. Labels should be concise.
- `aria-describedby`: ID reference(s) that describe the element; use for longer, more verbose information than a label. The referenced elements make up the entire description, so list several IDs or reference a wrapper element.
- `aria-current`: token marking the single current item in a set (`page`, `step`, `location`, `date`, `time`, `true`). Mark only one element in a set. Do not use it in place of `aria-selected` where selected has that meaning (for example a tab); the two can differ in a navigation tree (current page versus the treeitem that would open).
- `aria-hidden="true"`: element is hidden from the accessibility API (also hidden if an ancestor is). Hiding rendered content is allowed only with caution to remove redundant or extraneous content, and equivalent meaning and functionality must stay exposed; hiding visible link text can break voice control and type-ahead search.
- `aria-disabled="true"`: element is perceivable but not operable; it applies to the element and its focusable descendants. Authors should also change appearance. Disabled elements "might not receive focus from the tab order". Only use it where the host language cannot disable the element itself; in 1.2 it is being deprecated as a global state.

## Gotchas
- `aria-hidden="false"` is known to work inconsistently in browsers per the spec note.

## Verify
- [ ] State attributes change in the DOM in sync with the visual state.

## Checked

Method: 2026-11-09 docs-only; fetched WAI-ARIA 1.2 and read the definitions of aria-controls, aria-current, aria-describedby, aria-disabled, aria-hidden and the opening of aria-expanded and aria-labelledby. Removed unsourced claims about inconsistent aria-controls support, labelledby precedence over aria-label and the "never on focusable" rule for aria-hidden; the APG index source was dropped.
