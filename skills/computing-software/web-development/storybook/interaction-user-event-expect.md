---
id: computing-software.web-development.storybook.interaction-user-event-expect
name: interaction-user-event-expect
category: computing-software
field: web-development
product: storybook
tags: [userevent, expect-assertions, jest-dom, fn-spy, interactions-panel]
level: practitioner
status: docs-checked
description: "Simulate behavior with userEvent and assert with expect and spies in play functions."
sources:
  - https://storybook.js.org/docs/writing-tests/interaction-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# userEvent and expect

Goal: simulate input and assert outcomes.

`userEvent` is a play function argument. Always `await` its methods so they are logged in the Interactions panel:
- `click`, `dblClick`, `hover`, `unhover`
- `tab`, `keyboard('{Shift}')`
- `type(element, 'text')`, `clear(element)`
- `selectOptions(select, ['1', '2'])`, `deselectOptions(select, '1')`

`expect` is imported from `storybook/test`. It combines Vitest's `expect` with `@testing-library/jest-dom` matchers; always `await` it:

```ts
import { expect, fn } from 'storybook/test';

await expect(canvas.getByText('Hi')).toBeInTheDocument();
await expect(button).toBeVisible();
await expect(button).toHaveAttribute('aria-disabled', 'true');
await expect(args.onSubmit).toHaveBeenCalledWith('example');
```

Spy with `fn()` from `storybook/test`, usually as an arg value, then read it from `args` in `play`.

Full example:

```ts
export const FilledForm = meta.story({
  args: { onSubmit: fn() },
  play: async ({ args, canvas, userEvent }) => {
    await userEvent.type(canvas.getByLabelText('Email'), 'a@b.com');
    await userEvent.click(canvas.getByRole('button', { name: 'Log in' }));
    await expect(args.onSubmit).toHaveBeenCalled();
  },
});
```

The Interactions panel shows the step flow with controls to pause, resume, rewind and step through.

Verify: the panel lists each step and any failure points at the failing step.

## Checked
Date: 2026-11-04. Read the Interaction tests page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: userEvent method table, await requirement, `expect` import path and composition, `fn` usage, panel controls.
Fixed: the skill implied `expect` needs no import; it comes from `storybook/test`. Replaced an invented `toHaveBeenCalledWith` argument with the page's.
Method: documentation only; no commands were run.
