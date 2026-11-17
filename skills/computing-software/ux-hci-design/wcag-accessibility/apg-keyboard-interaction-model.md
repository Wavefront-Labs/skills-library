---
id: computing-software.ux-hci-design.wcag-accessibility.apg-keyboard-interaction-model
name: apg-keyboard-interaction-model
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [roving-tabindex, aria-activedescendant]
level: advanced
status: docs-checked
description: "Manage focus in composite widgets with roving tabindex or aria-activedescendant according to the APG."
sources:
  - https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing focus in composite widgets
- Tab and Shift+Tab move between components; arrow keys (authors choose keys but should copy OS conventions) move inside a composite widget. The composite contributes one element to the tab sequence.
- **Roving tabindex**: on load, `tabindex="0"` on the element to include in the tab sequence and `tabindex="-1"` on the other focusable elements. On a navigation key, set `-1` on the old element, `0` on the new one, then call `.focus()` on it. Benefit: the browser scrolls the newly focused element into view.
- **aria-activedescendant**: only the container is in the tab sequence and keeps DOM focus. Its `aria-activedescendant="IDREF"` names the active element, and you must draw the focus indicator and scroll the element into view yourself. The container's role must support the property, and the referenced element must be a DOM descendant of the container, be listed in its `aria-owns`, or (for a combobox, textbox or searchbox) sit under an element it points to with `aria-controls`.
- Where focus lands on Tab-in depends on the widget: last-focused element (grid, treegrid), selected element else first (radio group, tabs, listbox, tree), or first element (menubar, toolbar).
- Handle pointer clicks the same way as keys, setting tabindex or aria-activedescendant, so keyboard and pointer state do not mismatch.
- Selection is not focus: focus is the active element, selection is `aria-selected="true"`. The focus indicator must always be visible and selection visually distinct. Selection following focus suits instant tab panels but not panels that need network requests; otherwise Enter or Space selects.
- Disabled items: native `disabled` removes from the tab sequence; `aria-disabled="true"` keeps focus, which the APG uses for menu items, tabs, listbox options and tree items so screen reader users can discover them.
- Avoid positive `tabindex` values; reorder the DOM instead.

## Verify
- [ ] The widget is a single Tab stop; arrows move within.
- [ ] Focus is never lost to the body, for example after closing a dialog.

## Checked
2026-11-09. Read the whole APG "Developing a Keyboard Interface" page (w3.org/WAI/ARIA/apg/practices/keyboard-interface/) and confirmed the above. Removed the unsupported Home/End and type-ahead line. The page has unfinished sections (shortcuts, focus indicators); they are not summarised.

Method: documentation only; no commands were run.
