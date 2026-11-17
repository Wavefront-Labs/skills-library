---
id: computing-software.web-development.web-accessibility.character-key-shortcuts
name: character-key-shortcuts
category: computing-software
field: web-development
product: web-accessibility
tags: [keyboard-accessibility, character-key-shortcuts, wcag-2-1-4, keyboard-shortcuts, speech-input]
level: practitioner
status: verified
description: "Implementing single-character keyboard shortcuts safely under WCAG 2.1.4: turn-off or remap options, focus-only activation, modifier keys, and avoiding screen reader conflicts."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/accesskey
  - https://github.com/github/hotkey
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Character key shortcuts

**2.1.4 (A):** if a shortcut uses only letter, punctuation, number or symbol keys (e.g. `j`/`k`, `?`, `/` to search, `e` to archive), at least one is true:
- **Turn off**: a mechanism to disable it,
- **Remap**: a mechanism to change it to include a modifier (Ctrl, Alt, Cmd),
- **Active only on focus**: it only works when the relevant component has focus (e.g. list arrow keys, typeahead in a listbox).

## 1. Why
Speech-input users dictating text trigger shortcuts accidentally (saying "keep" types k-e-e-p -> four commands). Screen reader users' single-key navigation (H for headings in browse mode) can collide when the app captures keys. Tremor users hit keys accidentally.

## 2. Implementation
```js
const enabled = () => localStorage.getItem("shortcuts") !== "off";
document.addEventListener("keydown", e => {
  if (!enabled() || e.defaultPrevented || e.isComposing) return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const t = e.target;
  if (t.closest("input, textarea, select, [contenteditable], [role=textbox], [role=combobox]")) return;   // never while typing
  if (e.key === "/") { e.preventDefault(); searchInput.focus(); }
  if (e.key === "?") { openShortcutHelp(); }
});
```
- Settings page toggle "Keyboard shortcuts: on/off" (Gmail and GitHub provide this); remapping UI is a bonus.
- Show a `?` help dialog listing shortcuts.
- Modifier-based shortcuts (`Ctrl+K`) are outside this criterion but must not override browser/AT combos (Ctrl+L, Ctrl+T, Insert/CapsLock combos).
- Expose shortcuts to AT with `aria-keyshortcuts="/"` on the target element (informational).
- `accesskey` attribute: modifier keys differ by browser and platform and can collide with browser or AT shortcuts (see MDN) - avoid.

## 3. Libraries
`@github/hotkey` (its source returns early when the event target is a form field: input, textarea, select or contenteditable), `tinykeys`, `hotkeys-js` (skips INPUT, SELECT and TEXTAREA by default; `hotkeys.filter` customises that).

## Verify
With a speech-recognition tool (Windows Voice Access, macOS Voice Control) dictate in a non-input area - no unintended actions when shortcuts are off; toggle persists; shortcuts never fire while typing in fields.
