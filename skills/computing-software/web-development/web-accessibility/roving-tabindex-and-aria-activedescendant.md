---
id: computing-software.web-development.web-accessibility.roving-tabindex-and-aria-activedescendant
name: roving-tabindex-and-aria-activedescendant
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-accessibility, roving-tabindex, aria-activedescendant, composite-widgets, focus-management]
level: practitioner
status: docs-checked
description: "Managing focus inside composite widgets (toolbars, listboxes, grids, tabs) with roving tabindex or aria-activedescendant: one tab stop, arrow keys, Home/End and trade-offs."
sources:
  - https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/#kbd_general_within
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-activedescendant
  - https://www.w3.org/WAI/ARIA/apg/patterns/toolbar/
  - https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roving tabindex and aria-activedescendant

Composite widgets are **one Tab stop**; arrow keys move within them. Two techniques.

## 1. Roving tabindex (moves real DOM focus)
```js
function roving(container, itemSel, { orientation = "horizontal", wrap = true } = {}) {
  const items = () => [...container.querySelectorAll(itemSel)].filter(el => !el.disabled);
  items().forEach((el, i) => el.tabIndex = i === 0 ? 0 : -1);
  container.addEventListener("keydown", e => {
    const list = items(), i = list.indexOf(document.activeElement);
    if (i < 0) return;
    const prev = orientation === "horizontal" ? "ArrowLeft" : "ArrowUp";
    const next = orientation === "horizontal" ? "ArrowRight" : "ArrowDown";
    let j = { [prev]: i - 1, [next]: i + 1, Home: 0, End: list.length - 1 }[e.key];
    if (j === undefined) return;
    e.preventDefault();
    j = wrap ? (j + list.length) % list.length : Math.max(0, Math.min(j, list.length - 1));
    list[i].tabIndex = -1; list[j].tabIndex = 0; list[j].focus();
  });
}
roving(toolbar, "button");
```
- Remember the last active item (tabbing back returns to it).
- RTL: swap left/right.
- Pro: the browser scrolls the newly focused element into view (APG), and normal focus styling applies.

## 2. aria-activedescendant (focus stays on the container/input)
```html
<input role="combobox" aria-expanded="true" aria-controls="lb" aria-activedescendant="opt-3">
<ul role="listbox" id="lb"><li role="option" id="opt-3" aria-selected="true">Paris</li>…</ul>
```
- DOM focus remains on the input (user keeps typing); `aria-activedescendant` points at the visually highlighted option's id. Update it on arrow keys and style the active item yourself (`[aria-selected=true]` or a class) and scroll it into view (`scrollIntoView({ block: "nearest" })`).
- APG comboboxes with listbox, grid or tree popups keep DOM focus on the combobox and use this technique (a dialog popup receives DOM focus instead); it also suits other composites whose role supports it.
- The referenced element needs an id and should be a descendant of the focused element (for a combobox, an element in its popup referenced via `aria-controls`); browsers do not validate this.
- Con: DOM focus does not move, so you must style the active item and scroll it into view yourself; test with the assistive technology you support.

## 3. Which widget, which keys (APG)
Toolbar/radio group/tabs: arrows (Home/End optional in toolbars). Listbox/menu: up/down, type-ahead. Grid: all arrows, Ctrl+Home/End, Page Up/Down. Tree: up/down, right expands, left collapses.

## Verify
Only one Tab stop per widget; arrows move with visible focus; screen reader announces item name, role, position ("2 of 5") and state.

## Checked

- Date: 2026-10-26. Documentation: ARIA APG keyboard interface practice, toolbar, combobox, grid and treeview patterns, WAI-ARIA 1.2, MDN `aria-activedescendant`.
- Confirmed: roving tabindex algorithm (`tabindex="0"` on one element, `-1` on the rest); with roving tabindex the browser scrolls the focused element into view; with `aria-activedescendant` DOM focus stays on the container and assistive technology treats the referenced element as focused; ARIA does not require user agents to validate the descendant relationship; comboboxes with listbox, grid or tree popups use it; toolbar arrow keys with optional Home and End; grid Page Up and Control+Home; tree Right Arrow opens a closed node.
- Removed (no documentation found): the "works with any AT" claim and the VoiceOver iOS remark.
Method: documentation only; no commands were run.