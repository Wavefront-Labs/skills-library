---
id: computing-software.web-development.storybook.custom-render-functions
name: custom-render-functions
category: computing-software
field: web-development
product: storybook
tags: [render, custom-render, render-function, args-render, csf]
level: practitioner
status: docs-checked
description: "Control how a story renders with a render function at meta or story level while still passing args to the component."
sources:
  - https://storybook.js.org/docs/writing-stories/csf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom render functions

Goal: render more than the bare component for a story.

By default Storybook renders `meta.component` and passes the story `args` as props. Use `render` when you need a wrapper, children or composition. The first argument is `args`:

```tsx
const meta = preview.meta({
  component: Button,
  render: (args) => (
    <Alert>
      <Button {...args} />
    </Alert>
  ),
});

export const Primary = meta.story({ args: { primary: true } });
```

A `render` on meta applies to all stories in the file; a `render` on a single story overrides it for that story.

Tips:
- The second argument is the story context. `argTypes` and `hooks` are available there, as in decorators.
- Do not mix React hooks with Storybook hooks in render; use Storybook's equivalents from `storybook/preview-api`, and `useArgs` to hold state in args.
- In Svelte CSF, supply a custom snippet instead of a render function.

Verify: the canvas shows the wrapper, and Controls still change the inner component.

## Checked
Date: 2026-11-04. Read the CSF, Args and Decorators pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: render signature, meta versus story level, hooks warning, Svelte snippet.
Removed: a full list of context fields and a claim that render makes the Source block cleaner; the pages only say the latter about decorators.
Method: documentation only; no commands were run.
