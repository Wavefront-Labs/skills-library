---
id: computing-software.web-development.storybook.actions-fn-spies
name: actions-fn-spies
category: computing-software
field: web-development
product: storybook
tags: [actions, fn-spy, action-panel, event-handlers, argtypesregex]
level: practitioner
status: docs-checked
description: "Log event handler calls to the Actions panel with fn() spies, argTypesRegex, spyOn and the action function."
sources:
  - https://storybook.js.org/docs/essentials/actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Actions

Goal: see that callbacks were called and with what.

Recommended: assign `fn()` from `storybook/test` to handler args. It is a mock function Storybook spies on, so calls appear in the Actions panel and can be asserted in tests:

```ts
import { expect, fn } from 'storybook/test';

export const Clicked = meta.story({
  args: { onClick: fn() },
  play: async ({ args, canvas, userEvent }) => {
    await userEvent.click(canvas.getByRole('button'));
    await expect(args.onClick).toHaveBeenCalled();
  },
});
```

A `fn()` created outside `args` needs a name to log: `fn().mockName('handleClick')`.

Other options:
- `parameters.actions.argTypesRegex = '^on.*'` creates actions for matching argTypes (event format `<eventname> <selector>`). Not recommended: args inferred this way are not available as spies in play functions, so you must also define `fn()` args to assert on them.
- `spyOn` from `storybook/test` logs non-story function calls; the spy shows with a default name, customize it with `mockName`.
- `action('name')` from `storybook/actions` logs manually.
- `configureActions({ limit: 50, clearOnStoryChange: true, depth: 10 })` in the preview file (values shown are the defaults).

Parameters: `actions.disable`, `actions.expandLevel` (default 1), `actions.argTypesRegex`.

Verify: clicking the component adds an entry to the Actions panel.

## Checked
Date: 2026-11-04. Read the Actions page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: fn() recommendation, mockName, spyOn, action import path, configureActions defaults, expandLevel default.
Fixed: the reason argTypesRegex is discouraged (inferred args are not spies in play functions). Added the missing `expect` import in the example.
Method: documentation only; no commands were run.
