---
id: computing-software.web-development.frontend-development.keyboard-events-key-code-and-ime
name: keyboard-events-key-code-and-ime
category: computing-software
field: web-development
product: frontend-development
tags: [keyboard-events, ime-composition, event-key, event-code, keyboard-shortcuts, dom-events]
level: practitioner
status: docs-checked
description: "Handling keydown correctly: key vs code, modifier differences on macOS, IME composition (isComposing), repeat, beforeinput, and shortcuts that do not clash with assistive tech."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent
  - https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/isComposing
  - https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyboard events: key, code and IME

## 1. key vs code
| | `e.key` | `e.code` |
|---|---|---|
| Meaning | character / logical key after layout | physical key position |
| key labelled Z on AZERTY | `"z"` | `"KeyW"` (QWERTY position) |
| Use for | text shortcuts (`Ctrl+K`), Enter, Escape, arrows | games (WASD), layout-independent positions |
`keyCode`/`which`/`keypress` are deprecated; do not use.

## 2. Shortcuts
```js
addEventListener("keydown", e => {
  if (e.defaultPrevented || e.isComposing) return;
  const mod = e.metaKey || e.ctrlKey;   // pick one per platform if both must not trigger
  if (mod && e.key.toLowerCase() === "k") { e.preventDefault(); openSearch(); }
  if (e.key === "Escape") closePopover();
});
```
- Ignore shortcuts while focus is in `input`, `textarea`, `[contenteditable]` unless intended.
- Single-character shortcuts must be turned off, remapped, or active only on focus (WCAG 2.1.4 Character Key Shortcuts).
- `e.repeat` is true for auto-repeat; ignore it for toggles.
- Shift changes `key` (`"K"` vs `"k"`); normalise with `toLowerCase()`.

## 3. IME composition (Chinese, Japanese, Korean, some Android keyboards)
`KeyboardEvent.isComposing` is true for events fired after `compositionstart` and before `compositionend`. Pressing Enter to confirm a candidate must not submit:
```js
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.isComposing) submit();
});
```
`compositionstart` / `compositionupdate` / `compositionend` bracket the session; validate or filter text on `compositionend`, not mid-composition.

## 4. Text changes: use input events
For "what changed in the field", listen to `beforeinput` and `input`; `beforeinput` is not always cancelable and not every modification fires it (MDN lists autocomplete and spell-check corrections). Key events miss paste, autofill, dictation and IME output. `key` is `"Unidentified"` when the key cannot be identified.

## Gotchas
- `preventDefault` on Space in a focused button stops activation; on the page it stops scrolling.
- AltGr on Windows sends Ctrl+Alt; check `e.getModifierState("AltGraph")` before treating it as a shortcut.

## Verify
- [ ] Japanese IME: Enter selects a candidate without submitting.
- [ ] Shortcuts work on QWERTY and AZERTY; nothing fires while typing in fields.

## Checked

Checked 2026-10-26 against mdn/content (main) KeyboardEvent key, code, isComposing, keyCode and getModifierState pages, the beforeinput event page, and the W3C WCAG understanding documents for 2.1.4 and 2.5.7.

- Confirmed: `code` is a physical key unaffected by layout (the same code is Q on QWERTY and A on AZERTY); `key` is `"Dead"` for dead keys and `Unidentified` when unknown; `keyCode` is deprecated; `isComposing` covers events between `compositionstart` and `compositionend`; on Windows AltGraph raises ControlLeft and AltRight; WCAG 2.1.4 requires character-key shortcuts to be turned off, remapped or focus-only, and 2.5.7 requires a single-pointer alternative to dragging.
- Removed: the platform detection through `navigator.userAgentData`/`navigator.platform`, the `keyCode === 229` legacy check, the claim about screen reader keys, and the Android virtual keyboard remark, none of which the pages checked state.

Method: documentation only; no commands were run.
