---
id: computing-software.web-development.web-accessibility.apg-combobox-autocomplete
name: apg-combobox-autocomplete
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, combobox-pattern, autocomplete, listbox, aria-activedescendant]
level: practitioner
status: docs-checked
description: "Building an accessible combobox/autocomplete per ARIA 1.2: input with role=combobox, listbox popup, aria-activedescendant, live result counts, and selection behaviour."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
  - https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-autocomplete-list/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/appearance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combobox / autocomplete

## 1. Consider native first
`<select>` for short fixed lists (stylable with `appearance: base-select`, see MDN for current browser support); `<input list="dl">` + `<datalist>` for simple suggestions (limited styling, varies by browser). Build a custom combobox only for async search, rich options or custom filtering.

## 2. ARIA 1.2 structure
```html
<label for="city">City</label>
<input id="city" type="text" role="combobox" aria-autocomplete="list"
       aria-expanded="false" aria-controls="city-list" aria-activedescendant="" autocomplete="off">
<ul id="city-list" role="listbox" aria-label="Cities" hidden>
  <li id="city-opt-0" role="option" aria-selected="false">Paris</li>
</ul>
<div class="visually-hidden" role="status" aria-live="polite" id="city-count"></div>
```
- Focus **stays in the input**; `aria-activedescendant` points at the highlighted option.
- `aria-expanded` reflects popup visibility; `aria-controls` only needs to be set while the popup is visible. A popup that is not a listbox needs `aria-haspopup` (grid, tree or dialog); listbox is the implicit value.
- `aria-autocomplete`: `list` (suggestions), `both` (inline completion too), `none`.

## 3. Keyboard
- Down Arrow: if the popup is available, moves focus into it (the first option, or the one after an automatically selected suggestion). Up Arrow (optional): focus goes to the last option.
- Alt+Down Arrow (optional): shows the popup without moving focus. Alt+Up Arrow (optional): closes it.
- Enter: accepts the focused option, closes the popup and places the value in the input with the cursor at the end.
- Escape: closes the popup and returns focus to the input; optionally, when the popup is already hidden, it clears the combobox.
- Typing edits the input with the platform's standard text-editing keys.
- Tab: the combobox is in the page Tab sequence; the popup and its descendants are not.

## 4. Behaviour details
- Debounce async queries, cancel stale requests (AbortController) and ignore out-of-order responses.
- Announce counts politely: "5 results available" - debounced so it doesn't chatter.
- Highlight matched text with `<mark>` but keep the option's accessible name clean.
- Scroll the active option into view (`scrollIntoView({ block: "nearest" })`).
- Mouse/touch selection must update the input and close.
- Error/no results state: an option-less listbox isn't announced; use the status region ("No results").

## 5. Use a tested implementation
A maintained, tested library implementation is safer than a hand-rolled combobox; test whichever you pick against the APG keyboard model above.

## Verify
NVDA + Firefox/Chrome, JAWS, VoiceOver macOS and iOS: typing announces result count; arrows announce options; Enter selects; the input value is read back.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG combobox pattern: Down Arrow, Up Arrow, Alt+Down, Alt+Up, Enter, Escape and Tab behaviour, DOM focus staying on the input with aria-activedescendant, aria-controls only needed when the popup is visible, implicit listbox haspopup. Removed unconfirmed debounce timing, library list and audit-frequency claim; softened base-select browser support.

Method: documentation only; no commands were run.
