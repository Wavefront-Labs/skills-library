---
id: computing-software.web-development.web-accessibility.manual-keyboard-testing
name: manual-keyboard-testing
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-testing, manual-accessibility-testing, tab-order, focus-visible, wcag-2-1-1, accessibility-testing]
level: practitioner
status: docs-checked
description: "A repeatable manual keyboard test: browser setup (Safari tab setting), checking focus order, visibility, traps, operability, modals, hidden-but-focusable elements and reporting."
sources:
  - https://webaim.org/techniques/keyboard/
  - https://www.w3.org/WAI/test-evaluate/
  - https://firefox-source-docs.mozilla.org/devtools-user/accessibility_inspector/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual keyboard testing

Automated tools cannot tell whether a page is operable by keyboard. This test takes 10-20 minutes per template.

## 1. Setup
- Put the mouse/trackpad away.
- **Safari**: check the browser's and macOS's current keyboard navigation settings so that Tab reaches every control before you start.
- Firefox Accessibility Inspector > "Show Tabbing Order" shows the tabbing order as an overlay.
- Test at 100% and 200% zoom.

## 2. Procedure
1. Load the page; first Tab should reach a visible "Skip to content" link; activate it and confirm focus lands in main.
2. Tab through everything. At each stop check: focus is **visible** (2.4.7), not hidden under sticky headers (2.4.11), order follows the visual/reading order (2.4.3).
3. Watch for focus disappearing: focus on off-screen or hidden menus, collapsed accordions, carousels' hidden slides, `opacity: 0` elements. Fix with `inert`, `hidden`, or `visibility: hidden`.
4. Operate every control: Enter/Space on buttons, arrows in tabs/menus/radios/sliders, Escape on popups, type in comboboxes and choose options.
5. Dialogs: focus moves into the dialog, Tab cycles inside, Escape closes, focus returns to the trigger.
6. Hover-only features (tooltips, mega menus, card actions shown on hover) must appear on focus too (2.1.1, 1.4.13).
7. No keyboard traps (2.1.2): you can always Tab or Escape out of embeds, editors, maps, video players.
8. Drag-only interactions have a keyboard or single-pointer alternative (2.5.7).
9. Character-key shortcuts can be turned off or remapped (2.1.4).

## 3. Record findings
For each issue: page, element (selector/screenshot), steps, expected vs actual, WCAG SC, severity. Group repeated component issues once with all locations.

## Verify
- [ ] Every interactive feature on the template was reached and operated with the keyboard alone; issues logged with SC references.

## Checked

- Date: 2026-10-26. Documentation: WCAG 2.2 success criteria, WebAIM keyboard techniques, Firefox Source Docs (Accessibility Inspector).
- Confirmed: success criteria cited are 2.4.7 Focus Visible (AA), 2.4.11 Focus Not Obscured (Minimum) (AA), 2.4.3 Focus Order (A), 2.1.2 No Keyboard Trap (A), 2.5.7 Dragging Movements (AA), 2.1.4 Character Key Shortcuts (A), 1.4.13 (AA); the Firefox "Show Tabbing Order" checkbox exists; WebAIM advises a skip link, warns about `outline: none` and keyboard traps and says Esc should release a trap.
- Removed (no documentation found): the exact Safari and macOS setting paths and the "numbered" overlay description; the unverified W3C page anchor was replaced by the section root.
Method: documentation only; no commands were run.