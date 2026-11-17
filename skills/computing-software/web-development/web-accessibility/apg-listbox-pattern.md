---
id: computing-software.web-development.web-accessibility.apg-listbox-pattern
name: apg-listbox-pattern
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-listbox, aria-selected, aria-multiselectable, type-ahead, apg-patterns, custom-select]
level: advanced
status: docs-checked
description: "Implementing the ARIA listbox: single and multi-select keyboard models, aria-selected vs focus, activedescendant or roving tabindex, type-ahead, grouping, and when to use select."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/listbox/
  - https://www.w3.org/WAI/ARIA/apg/patterns/listbox/examples/listbox-scrollable/
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/listbox_role
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listbox pattern

Use a native `<select>` (single) or checkboxes (multi) unless you need rich option content; a custom listbox is a lot of behaviour to get right.

## 1. Markup
```html
<span id="lb-label">Transport</span>
<ul role="listbox" id="lb" tabindex="0" aria-labelledby="lb-label" aria-activedescendant="opt-bus">
  <li role="option" id="opt-car" aria-selected="false">Car</li>
  <li role="option" id="opt-bus" aria-selected="true">Bus</li>
  <li role="option" id="opt-bike" aria-selected="false" aria-disabled="true">Bike</li>
</ul>
```
- Focus stays on the listbox; `aria-activedescendant` points at the visually focused option (or move DOM focus among options with roving tabindex). In a multi-select listbox set `aria-multiselectable="true"`; use either aria-selected or aria-checked consistently, not both.
- Groups: `role="group"` with `aria-labelledby` wrapping options.
- Keep the active option scrolled into view (`scrollIntoView({ block: "nearest" })`).

## 2. Keyboard: single select
| Key | Action |
|---|---|
| Down / Up | move focus (selection usually follows focus) |
| Home / End | first / last option (optional; strongly recommended for lists of more than five options) |
| Type characters | jump to the next option starting with the typed character or string (recommended for all listboxes; APG gives no buffer duration) |

## 3. Keyboard: multi select (`aria-multiselectable="true"`)
| Key | Action |
|---|---|
| Down / Up | move focus without changing selection |
| Space | toggle selection of the focused option |
| Shift+Down / Shift+Up (optional) | move focus and toggle selection of the next / previous option |
| Shift+Space (optional) | select contiguous options from the last selected to the focused one |
| Ctrl+A (optional) | select all (a separate Select all button is more accessible) |
| Ctrl+Shift+Home / End (optional) | select from the focused option to the first / last |

APG also describes a second model that needs Ctrl: Ctrl+Down / Ctrl+Up move focus without changing selection and Ctrl+Space toggles; the Space-only model above is the recommended one.
Every option carries `aria-selected="true|false"` so unselected state is announced.

## 4. Visual
Focus and selection need distinct visuals (outline for focus, background/check for selected), never colour alone. Handle disabled options consistently (focusable but not selectable, or skipped).

## 5. Inside a combobox
A listbox popup of a combobox keeps DOM focus on the input with `aria-activedescendant` on the input; see the combobox pattern.

## Verify
- [ ] NVDA/VoiceOver announce "Bus, selected, 2 of 3"; multi-select announces "not selected" for unselected options; type-ahead works.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG listbox pattern: Down/Up/Home/End, type-ahead, the recommended Space-toggle multi-select model and the optional Shift/Ctrl shortcuts, aria-multiselectable, aria-selected false on unselected options, aria-activedescendant support, group role for option groups, selection follows focus in single-select. Removed the unconfirmed 500 ms type-ahead buffer, corrected Shift+arrow semantics, and removed the claim that APG makes disabled options focusable.

Method: documentation only; no commands were run.
