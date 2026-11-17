---
id: computing-software.web-development.storybook.controls-types
name: controls-types
category: computing-software
field: web-development
product: storybook
tags: [controls, control-types, argtypes-control, radio, select]
level: practitioner
status: docs-checked
description: "Pick the right control type for each arg: boolean, number, range, object, radio, check, select, text, color, date, file."
sources:
  - https://storybook.js.org/docs/essentials/controls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Controls: control types

Goal: give each arg an appropriate input in the Controls panel.

Storybook infers controls from the component and arg values when `component` is set in meta. Override with `argTypes`:

```ts
argTypes: {
  variant: { control: 'radio', options: ['primary', 'secondary'] },
  size: { control: { type: 'range', min: 1, max: 30, step: 3 } },
  accent: { control: { type: 'color', presetColors: ['red', 'green'] } },
}
```

| Data type | Control |
| --- | --- |
| boolean | `boolean` |
| number | `number` (min, max, step) or `range` |
| object, array | `object` (JSON editor, raw mode) |
| array of URLs | `file` (`accept: '.png'`) |
| enum | `radio`, `inline-radio`, `check`, `inline-check`, `select`, `multi-select` (need `options`) |
| string | `text`, `color`, `date` |

Notes:
- Numeric data defaults to a `number` control.
- The `date` control converts the picked date to a UNIX timestamp; convert it in your story if you need a Date.
- The `file` control returns an array of URLs.
- Automatic matching by arg name: names ending in `background` or `color` get a color picker, names ending in `Date` a date picker. Change with `parameters.controls.matchers`.
- For complex values use `mapping` and `control.labels`.

Verify: the panel shows the intended widget for each arg.

## Checked
Date: 2026-11-04. Read the Controls page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: control type table, matcher defaults, number default, date timestamp, file result.
Method: documentation only; no commands were run.
