---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-keyboard-operability-and-focus-order
name: designing-keyboard-operability-and-focus-order
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [focus-order, keyboard-operability, keyboard-navigation, tab-order, keyboard-accessibility, no-keyboard-trap]
level: practitioner
status: docs-checked
description: "Design keyboard operability: all functions reachable by keyboard, logical focus order, no traps, skip links, and composite widget key patterns."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
  - https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html
  - https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
  - https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keyboard operability and focus order

## Requirements
- **SC 2.1.1 Keyboard (A):** all functionality is operable through a keyboard interface, except where the underlying function depends on the path of the user's movement and not just the endpoints.
- **SC 2.1.2 No Keyboard Trap (A):** focus can be moved away from any component using the keyboard.
- **SC 2.4.1 Bypass Blocks (A):** a mechanism is available to bypass blocks of content repeated on multiple pages (a skip link is one way).
- **SC 2.4.3 Focus Order (A):** where navigation order affects meaning or operation, focusable components receive focus in an order that preserves meaning and operability.

## Design
1. **Reading order = focus order:** follow the visual layout and logical sequence; the ARIA Authoring Practices strongly advise against positive `tabindex` values.
2. **Use native elements** (button, a, input, select), which are focusable and keyboard-operable by default; custom controls need role, key handling and focus management.
3. **Composite widgets** (tabs, menus, grids, radio groups) use one tab stop plus arrow keys inside; the APG describes a roving `tabindex` and `aria-activedescendant` as the two ways to manage focus inside them.
4. **Modal dialogs (APG):** focus moves into the dialog on open, Tab wraps from the last to the first tabbable element inside it, Escape closes it, and on close focus returns to the invoking element unless that no longer exists.
5. **Skip link** to main content near the start of the page.
6. **Dynamic content:** when inserting content or changing views, move focus intentionally (to a heading or the new content) so keyboard and screen reader users are not lost.
7. **Document the order** on wireframes (numbered focus order) and the key bindings for custom components.

## Test
Unplug the mouse; use Tab, Shift+Tab, Enter, Space, arrows, Esc across each flow.

## Verify
- [ ] Every action can be done with the keyboard.
- [ ] Focus never disappears or gets trapped.
- [ ] Focus order matches reading order in every state.

## Checked
2026-11-01. Confirmed against the W3C Understanding pages for SC 2.1.1, 2.1.2, 2.4.1 and 2.4.3 (all level A) and the APG keyboard-interface and modal-dialog pages: criterion wording, the tabindex advice, roving tabindex and activedescendant, and the dialog key behaviour. Removed: the claim that the skip link must be the first focusable element.
Method: documentation only; no commands were run.
