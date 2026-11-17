---
id: computing-software.web-development.web-accessibility.apg-tabs-pattern
name: apg-tabs-pattern
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, tabs-pattern, tablist, roving-tabindex, wai-aria-apg]
level: practitioner
status: verified
description: "Implementing the APG tabs pattern: tablist/tab/tabpanel roles, aria-selected, roving tabindex with arrow keys, automatic vs manual activation, and when not to use tabs."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
  - https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/
  - https://adrianroselli.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tabs pattern

## 1. Markup
```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" id="t-profile" aria-selected="true" aria-controls="p-profile">Profile</button>
  <button role="tab" id="t-security" aria-selected="false" aria-controls="p-security" tabindex="-1">Security</button>
</div>
<div role="tabpanel" id="p-profile" aria-labelledby="t-profile" tabindex="0">…</div>
<div role="tabpanel" id="p-security" aria-labelledby="t-security" tabindex="0" hidden>…</div>
```

## 2. Keyboard
- Tab enters the tablist on the **selected** tab (roving tabindex); next Tab moves into the active panel.
- Left/Right arrows move between tabs, wrapping (Up/Down for `aria-orientation="vertical"`; a horizontal tablist does not listen for Up/Down). Home and End (first/last tab) are optional in the APG.
- **Automatic activation** (arrow selects and shows panel) when panels render instantly; **manual activation** (arrow moves focus, Enter/Space selects) when switching is slow (network fetch).
- `tabindex="0"` on the panel lets keyboard users reach panels without focusable content; drop it if the panel starts with a focusable element.

## 3. JS core
```js
function select(tab) {
  for (const t of tabs) {
    const on = t === tab;
    t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1;
    document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
  }
  tab.focus();
}
```
RTL: arrow directions swap. Run in Chromium: this `select()` leaves exactly one tab with `tabIndex` 0 and the AX tree shows "Security [selected]" with its tabpanel.

## 4. When not to use tabs
- Site navigation that changes URL/page - use links with `aria-current="page"` (styled as tabs is fine).
- Steps in a sequence - use a stepper/progress list.
- Content users need to compare - show it together.
- Deep-linkable sections: if tabs reflect URL state, sync `?tab=security` and handle back/forward.

## 5. Responsive
Many tabs overflowing on mobile: horizontal scroll of the tablist (keep arrows working) or switch to an accordion with the same content.

## Verify
Screen reader announces "Profile, tab, selected, 1 of 2"; one Tab stop for the tablist; arrows switch tabs; panel is reachable with Tab.
