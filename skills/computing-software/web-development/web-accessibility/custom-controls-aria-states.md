---
id: computing-software.web-development.web-accessibility.custom-controls-aria-states
name: custom-controls-aria-states
category: computing-software
field: web-development
product: web-accessibility
tags: [name-role-value, wcag-robust, aria-states, aria-expanded, aria-pressed, aria-checked, aria-selected, aria-current, wcag-4-1-2, custom-widgets]
level: practitioner
status: docs-checked
description: "Exposing state on custom controls (WCAG 4.1.2): aria-expanded, aria-pressed, aria-checked, aria-selected, aria-current, aria-disabled, kept in sync with UI."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://www.w3.org/TR/wai-aria-1.2/#state_prop_def
  - https://www.w3.org/WAI/ARIA/apg/patterns/button/
  - https://github.com/web-platform-dx/web-features/blob/main/features/switch-control.yml.dist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom controls: exposing ARIA states

**Goal:** assistive tech knows not just what a control is but its current state, and that state updates when the UI changes.

## 1. State attributes by widget
| Widget | State | Example |
|---|---|---|
| Disclosure / accordion / menu button | `aria-expanded="true|false"` on the **trigger** | `<button aria-expanded="false" aria-controls="faq1">` |
| Toggle button (Bold, Mute) | `aria-pressed="true|false|mixed"` | Name stays constant ("Mute"), state changes |
| Custom checkbox / switch | `role="checkbox"`/`"switch"` + `aria-checked` | Prefer native `<input type=checkbox>` |
| Tabs, listbox options, grid cells | `aria-selected` | On `role="tab"` / `"option"` |
| Current page in nav / step | `aria-current="page"|"step"|"date"` | On the link |
| Disabled but focusable | `aria-disabled="true"` | Keeps it discoverable; you must block activation |
| Invalid field | `aria-invalid="true"` | With an error message via `aria-describedby` |
| Busy region | `aria-busy="true"` | While loading content |
| Sort | `aria-sort` on the active `<th>` | `ascending`/`descending` |

## 2. Rules
- **Don't change the name to express state** for toggle buttons ("Mute" -> "Unmute" plus `aria-pressed` double-states). Either change the label and drop `aria-pressed`, or keep the label and use `aria-pressed`.
- Put `aria-expanded` on the control, not the panel.
- State values are the strings "true"/"false"; omitting `aria-expanded` is not the same as "false" (an undefined value means the element is not expandable).
- Keep visual state and ARIA state from the same source of truth (derive both from component state).
- CSS can style from ARIA: `[aria-expanded="true"] .chevron { rotate: 180deg }` - keeps them in sync by construction.

## 3. Native first
`<details>/<summary>` has expanded state built-in; `<input type="checkbox" switch>` (Safari 17.4 and later only, not Baseline at the check date) or a plain checkbox; `<dialog>`, `<select>`, `<button>` - native elements get name, role and state for free.

## Verify
- [ ] Accessibility tree (DevTools) shows correct role and state before and after interaction.
- [ ] Screen reader announces "collapsed/expanded", "pressed/not pressed", "checked/not checked" on toggle.
- [ ] axe passes `aria-allowed-attr`, `aria-valid-attr-value`.

## Checked

- Date: 2026-10-26. Documentation: WAI-ARIA 1.2, ARIA APG button pattern, web-features data, WCAG 2.2 Name, Role, Value.
- Confirmed: `aria-pressed` accepts true, false and mixed and the toggle label must not change with state (APG); an undefined `aria-expanded` means not expandable; `aria-current`, `aria-sort`, `aria-selected`, `aria-busy` and `aria-invalid` exist as listed; `<input type="checkbox" switch>` is Safari 17.4+ only in web-features.
- Removed: the React rendering remark (no documentation checked).
Method: documentation only; no commands were run.