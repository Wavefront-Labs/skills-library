---
id: computing-software.web-development.frontend-development.select-datalist-and-optgroup
name: select-datalist-and-optgroup
category: computing-software
field: web-development
product: frontend-development
tags: [datalist-element, select-optgroup, select-element, html-forms, combobox-native]
level: practitioner
status: docs-checked
description: "Choosing between select, select multiple, optgroup and input+datalist for choice controls; placeholder options, required, reading values and datalist limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/datalist
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/optgroup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# select, optgroup and datalist

## 1. Pick the control
| Need | Control |
|---|---|
| One of 2-5 visible options | radio group in `fieldset` |
| One of many fixed options | `<select>` |
| Several of many | checkboxes (best) or `<select multiple>` (poor UX on desktop) |
| Free text with suggestions | `<input list>` + `<datalist>` |
| Async search, rich rows | ARIA combobox (see APG) |

## 2. select done right
```html
<label for="country">Country</label>
<select id="country" name="country" required autocomplete="country">
  <option value="">Choose a country</option>
  <optgroup label="Europe">
    <option value="GB">United Kingdom</option>
    <option value="IE">Ireland</option>
  </optgroup>
</select>
```
- `required` + an empty-value first option = placeholder that fails validation if left.
- `optgroup` labels are not selectable; no nested optgroups.
- `<hr>` inside `<select>` adds a separator between options; it is decorative and not exposed to assistive technology.

## 3. datalist
```html
<label for="browser">Browser</label>
<input id="browser" name="browser" list="browsers">
<datalist id="browsers"><option value="Firefox"><option value="Safari"><option value="Chrome"></datalist>
```
- Suggestions only: any text is accepted; validate server-side.
- Works on text, search, url, tel, email, number, the date and time types and range (range shows tick marks), so use an APG combobox when you need full control of the suggestion list.

## Gotchas
- `select.value` is the empty string when no option is selected.
- `<select multiple>` sends repeated `name=value` pairs; the server must read all of them as a list.
- `size` > 1 turns a select into a listbox.

## Verify
- [ ] Submitting without choosing triggers the native required message.
- [ ] Keyboard: type-ahead letters jump to options; arrow keys change selection.

## Checked
2026-10-26. MDN select, optgroup, datalist and HTMLSelectElement.value pages (main, 2026-10-26): confirmed optgroup cannot be nested, hr separators inside select (decorative, not in the accessibility tree), the empty-value first option as placeholder for a required single select, multiple submits repeated name=value pairs, size greater than 1 gives a listbox, and the input types datalist supports. Removed unconfirmed styling and screen-reader remarks, the framework parameter names and the Option/add API note.
Method: documentation only; no commands were run.
