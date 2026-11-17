---
id: computing-software.web-development.web-accessibility.apg-tree-view-pattern
name: apg-tree-view-pattern
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-treeview, apg-tree, role-tree, treeitem, keyboard-navigation]
level: advanced
status: docs-checked
description: "Implementing the APG tree view: tree/treeitem/group roles, aria-expanded and aria-level, roving tabindex, arrow keys and typeahead, and when to avoid trees."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/treeview/
  - https://www.w3.org/WAI/ARIA/apg/patterns/treeview/examples/treeview-navigation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tree view pattern

A tree is a desktop-style widget (file explorers, nested folders). For site navigation, nested disclosure lists of links are usually simpler and better supported: screen readers switch to focus mode inside a tree and users must know tree keys.

## 1. Markup
```html
<ul role="tree" aria-label="Files">
  <li role="treeitem" aria-expanded="true" aria-selected="false" tabindex="0">src
    <ul role="group">
      <li role="treeitem" aria-selected="false" tabindex="-1">index.ts</li>
      <li role="treeitem" aria-expanded="false" tabindex="-1">lib
        <ul role="group" hidden>...</ul></li>
    </ul></li>
</ul>
```
- Parent nodes carry `aria-expanded`; end nodes must not have it, or assistive technology would describe them as parents.
- When the DOM nesting doesn't reflect levels (virtualised flat lists), declare `aria-level`, `aria-setsize`, `aria-posinset` on each treeitem; browsers can compute them from DOM structure in the APG computed-properties example.
- Multi-select trees: `aria-multiselectable="true"` on the tree and `aria-selected`/`aria-checked` on items.
- Give each parent treeitem an explicit name (for example wrap its label in a span and reference it with `aria-labelledby`) so the name does not depend on nested children's text.

## 2. Keyboard (roving tabindex: one item `tabindex=0`)
| Key | Action |
|---|---|
| Down / Up | next / previous visible item |
| Right | closed parent: expand; open parent: move to first child; leaf: nothing |
| Left | open parent: collapse; child: move to parent |
| Home / End | first / last focusable node, without opening or closing nodes |
| Enter | activates the node (default action); Space toggles selection of the focused node in the recommended multi-select model |
| Type characters | move to next item starting with that text |
| `*` | expand all siblings (optional) |

## 3. Implementation notes
- Compute the "visible items" list on each key press (skip children of collapsed nodes).
- Selection follows focus only in single-select trees where that is harmless; otherwise separate focus and selection.

## 4. Testing
Test with the screen readers you support and verify keyboard behaviour against the APG example.

## Verify
- [ ] All keys in the table behave as specified; level/position announced; only one tab stop for the whole tree; collapsed children unreachable.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG tree view pattern: Down/Up, Right and Left on closed/open parents and end nodes, Home/End, Enter, type-ahead, the optional asterisk to expand siblings, Space toggling in the recommended multi-select model, aria-expanded only on parent nodes, aria-selected or aria-checked used consistently, aria-level/setsize/posinset declared or computed, and selection following focus only in single-select. Removed the unconfirmed aria-busy, accessible-name computation and screen-reader announcement claims.

Method: documentation only; no commands were run.
