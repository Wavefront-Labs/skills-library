---
id: computing-software.ux-hci-design.wcag-accessibility.apg-combobox-menu-button
name: apg-combobox-menu-button
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [apg-combobox, apg-menu-button]
level: advanced
status: docs-checked
description: "Build combobox (autocomplete) and menu button widgets with the APG keyboard model and aria-activedescendant."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
  - https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/
  - https://www.w3.org/WAI/ARIA/apg/patterns/menubar/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combobox
- `role="combobox"` on the element that shows the value, with `aria-controls` pointing to the popup (`listbox`, `tree`, `grid` or `dialog`), `aria-expanded` false/true, and `aria-autocomplete` of `none`, `list` or `both`. Set `aria-haspopup` to grid, tree or dialog when the popup is not a listbox (listbox is the implicit value). Use a native label, else `aria-labelledby`, else `aria-label`.
- For listbox, grid and tree popups DOM focus stays on the combobox and `aria-activedescendant` points at the focused popup item; the selected option has `aria-selected="true"`. Dialog popups instead take DOM focus.
- Tab: only the combobox is in the tab sequence (the popup, its contents and any open button are excluded).
- Down Arrow moves into the popup (to the item after an auto-selected suggestion, else the first); Up Arrow optionally goes to the last. Escape closes the popup (optionally clears the field if it was already closed). Enter accepts the selected suggestion. Alt+Down Arrow optionally opens the popup without moving focus.
- In a listbox popup, Down/Up move and select the next/previous option, Enter accepts and closes, Escape closes and returns focus to the combobox, and printable characters on an editable combobox return focus to the input.
- Unlike a single-select listbox, a combobox lets users browse the popup and press Escape without losing the earlier value.

# Menu button
Roles: a `button` with `aria-haspopup="menu"` (or `true`), `aria-expanded` true while the menu shows and false when hidden, and optional `aria-controls` pointing to the `menu`. Enter or Space opens the menu and focuses the first item; Down Arrow (optional) does the same and Up Arrow (optional) focuses the last item. In the menu, Down/Up move between items (wrapping is optional), Right Arrow opens a submenu, Left Arrow closes one, and Escape closes the menu and returns focus to the button. Disabled items stay focusable. Focus inside the menu is managed either by `aria-activedescendant` on the menu or by tabindex `-1` on each item with `element.focus()`. The APG also shows a navigation menu button whose items behave as links.

## Verify
- [ ] Complete selection by keyboard only; Escape closes the popup or menu and returns focus to the combobox or button.

## Checked
2026-11-09. Read the APG Combobox and Menu Button pattern pages in full and the Menu and Menubar pattern page in full (the menu button page defers menu key behaviour to it, so it was added as a source). Removed the unsupported live-region result-count claim and the claim that role="menu" is not for site navigation (the APG has a navigation menu button example).

Method: documentation only; no commands were run.
