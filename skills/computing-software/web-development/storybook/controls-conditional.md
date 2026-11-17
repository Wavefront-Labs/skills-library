---
id: computing-software.web-development.storybook.controls-conditional
name: controls-conditional
category: computing-software
field: web-development
product: storybook
tags: [conditional-controls, control-if, argtypes-if, arg-visibility, controls-query]
level: advanced
status: docs-checked
description: "Show or hide a control depending on another arg or global with the if query object."
sources:
  - https://storybook.js.org/docs/essentials/controls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditional controls

Goal: hide advanced controls until a related control is set.

Add `if` to an argType. The query names a target with exactly one of `arg` or `global`, plus at most one operator:

| field | meaning |
| --- | --- |
| `arg` | id of the arg to test |
| `global` | id of the global to test |

| operator | meaning |
| --- | --- |
| `truthy` | target is truthy |
| `exists` | target is defined |
| `eq` | target equals the value |
| `neq` | target does not equal the value |

With no operator it is `{ truthy: true }`.

```ts
argTypes: {
  advanced: { control: 'boolean' },
  // only shown when advanced is on
  margin: { control: 'number', if: { arg: 'advanced' } },
  // mutual exclusion: hidden when image is set
  label: { control: 'text', if: { arg: 'image', truthy: false } },
}
```

Use it to keep large control panels manageable or to prevent contradictory combinations.

Verify: toggling `advanced` shows and hides the `margin` control.

## Checked
Date: 2026-11-04. Read the Controls page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: `arg`/`global` fields, operator table, default `{ truthy: true }`.
Fixed: replaced an invented `global: 'viewport.value'` example with the page's `advanced` and mutual-exclusion examples.
Method: documentation only; no commands were run.
