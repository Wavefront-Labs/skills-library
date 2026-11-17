---
id: computing-software.web-development.frontend-development.labels-fieldsets-and-control-grouping
name: labels-fieldsets-and-control-grouping
category: computing-software
field: web-development
product: frontend-development
tags: [html-forms, form-labels, fieldset-legend, radio-groups, checkbox-groups, aria-describedby, hint-text, accessible-forms]
level: practitioner
status: docs-checked
description: "Labelling every control, grouping radios/checkboxes with fieldset and legend, and wiring hint text so forms read correctly in screen readers."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/fieldset
  - https://www.w3.org/WAI/tutorials/forms/labels/
  - https://www.w3.org/WAI/tutorials/forms/grouping/
  - https://design-system.service.gov.uk/components/fieldset/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Labels, fieldsets and grouping controls

**Goal:** every control has a visible, programmatic label and grouped controls announce their question.

## 1. One `<label>` per control
- Explicit: `<label for="email">Email</label><input id="email">` (ids must be unique - duplicated ids from repeated components are a frequent break).
- Implicit wrap: `<label><input type="checkbox"> Remember me</label>` - fine, and gives a larger click target.
- Placeholder is **not** a label; keep a visible `<label>`.
- `aria-label` only when a visible label truly can't exist (search icon field); the visible text should otherwise be the label (WCAG 2.5.3).

## 2. Group related controls
```html
<fieldset>
  <legend>Delivery speed</legend>
  <label><input type="radio" name="speed" value="std" checked> Standard (3-5 days)</label>
  <label><input type="radio" name="speed" value="exp"> Express (next day)</label>
</fieldset>
```
Use fieldset/legend for: radio groups, checkbox groups, and multi-input questions (date of birth day/month/year, address blocks). The legend is announced when entering the group. Keep legends short; on single-question pages make the legend the page heading (`<legend><h1>…</h1></legend>`).

Styling: fieldset has odd default rendering (`min-inline-size: min-content` blows out flex/grid). Reset with `fieldset { border:0; padding:0; margin:0; min-inline-size:0 }`.

## 3. Hints and errors
```html
<label for="ni">National Insurance number</label>
<p id="ni-hint" class="hint">For example, QQ 12 34 56 C</p>
<input id="ni" aria-describedby="ni-hint ni-error">
<p id="ni-error" class="error">Enter a National Insurance number in the correct format</p>
```
`aria-describedby` takes a space-separated id list read after the label. Only reference ids that exist (remove the error id when there is no error).

## 4. Required and optional
Mark required with the `required` attribute (announced) and visible text; if most fields are required, mark the optional ones "(optional)" instead.

## Verify
- [ ] Clicking each label focuses/toggles its control.
- [ ] Screen reader: entering a radio group announces the legend, then the option.
- [ ] axe reports no "form elements must have labels" and no duplicate ids.

## Checked
2026-10-26. MDN fieldset page and the GOV.UK Design System fieldset page (main, 2026-10-26): confirmed the legend is the first nested legend element and captions the group, fieldset has min-inline-size: min-content by default, and a single-question page can use the legend as the page heading. aria-describedby and WCAG 2.5.3 behaviour was not re-fetched; removed the unconfirmed placeholder-contrast detail.
Method: documentation only; no commands were run.
