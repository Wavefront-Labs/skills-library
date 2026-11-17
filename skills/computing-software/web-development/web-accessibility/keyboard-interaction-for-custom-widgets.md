---
id: computing-software.web-development.web-accessibility.keyboard-interaction-for-custom-widgets
name: keyboard-interaction-for-custom-widgets
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-interaction, apg-keyboard-conventions, composite-widgets, focus-mode, wcag-2-1-1, keyboard-accessibility]
level: practitioner
status: docs-checked
description: "Keyboard conventions custom widgets must follow: Tab between widgets, arrows within composites, Enter vs Space, Escape, Home/End, type-ahead, and screen reader focus mode."
sources:
  - https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
  - https://www.w3.org/WAI/ARIA/apg/patterns/grid/
  - https://www.w3.org/WAI/ARIA/apg/patterns/listbox/
  - https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
  - https://webaim.org/techniques/keyboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard interaction for custom widgets

Users expect the same keys to do the same things everywhere. Native elements already follow these; custom widgets must copy them.

## 1. The core conventions
| Key | Expected |
|---|---|
| Tab / Shift+Tab | move between widgets (one tab stop per composite widget) |
| Arrow keys | move within a composite: tabs, radio group, menu, menubar, listbox, tree, grid, toolbar |
| Enter | activate links and buttons; submit forms; open menu items |
| Space | activate buttons, toggle checkboxes/switches, select options; scrolls the page if nothing handles it |
| Escape | close popups/dialogs/menus and return focus to the trigger |
| Home / End | first / last item in a composite |
| Printable characters | type-ahead to an item in listbox, menu, tree |
| Page Up / Down | larger steps in grids (author-determined row count) and similar widgets; see each pattern |

## 2. Links vs buttons
Links navigate (Enter only); buttons act (Enter and Space). A `div` with `onClick` gets neither; a link styled as a button that submits forms confuses users. Use the right element; if you must use a role, implement the matching keys:
```js
el.addEventListener("keydown", e => {
  if (e.key === "Enter" || e.key === " ") { e.preventDefault(); el.click(); }
});
```

## 3. Composite widgets
One tab stop, arrows inside: implement with roving `tabindex` (only the active item `tabindex="0"`, others `-1`) or `aria-activedescendant` on the container. Arrow behaviour wraps or stops consistently; orientation set via `aria-orientation` when vertical/horizontal is not obvious.

## 4. Screen reader modes
Screen readers that have reading and interaction modes intercept navigation keys in reading mode. Widget roles trigger the interaction mode (APG disclosure navigation example), so use the correct widget role for composite widgets; content with no widget role stays in reading mode and may not receive your key handlers. Test with the screen readers you support.

## 5. Do not break the platform
Never trap Tab inside non-modal widgets, override browser/AT shortcuts (Ctrl+F, Ctrl+L, screen reader keys), or require key chords for basic actions.

## Verify
- [ ] Each custom widget has a key table in its docs matching APG, and a test pressing those keys.

## Checked

- Date: 2026-10-26. Documentation: ARIA APG keyboard interface practice and the grid, listbox, treeview, toolbar and menu button patterns.
- Confirmed: one tab stop per composite with arrows inside (roving tabindex or `aria-activedescendant`); Escape closes a modal dialog; Home and End move to the first and last cell in a grid row, Control+Home and Control+End to the first and last cell; Page Up and Page Down move an author-determined number of rows; type-ahead is recommended for listboxes and trees; widget roles trigger screen reader interaction mode.
- Removed (no documentation found): the Space-keyup remark, the NVDA and JAWS naming and the `role="application"` advice.
Method: documentation only; no commands were run.