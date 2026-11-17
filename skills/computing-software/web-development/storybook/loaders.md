---
id: computing-software.web-development.storybook.loaders
name: loaders
category: computing-software
field: web-development
product: storybook
tags: [loaders, async-data, loaded-context, global-loaders, loader-order]
level: advanced
status: docs-checked
description: "Load async data before a story renders with loaders and read it from the loaded context field."
sources:
  - https://storybook.js.org/docs/writing-stories/loaders
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Loaders

Goal: fetch or prepare data before a story and its decorators render.

Loaders are async functions that run before the story renders. Results land in the `loaded` field of the story context, the second argument of a story function. They are an advanced escape hatch: args are the recommended way to manage story data, and loaded data may not be compatible with the tooling built around args.

```tsx
export const Default = meta.story({
  loaders: [
    async () => ({
      todo: await (await fetch('https://jsonplaceholder.typicode.com/todos/1')).json(),
    }),
  ],
  render: (args, { loaded: { todo } }) => <TodoItem {...args} {...todo} />,
});
```

Global loaders go in the `loaders` export of the preview file, for example loading a current user available as `loaded.currentUser` in every story.

Inheritance:
- All loaders from all levels run in parallel before rendering.
- All results go into the `loaded` field.
- If keys overlap, later wins, lowest to highest: global loaders, component loaders, story loaders, each in the order defined.

Verify: `loaded` contains the fetched value in the render function.

## Checked
Date: 2026-11-04. Read the Loaders page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: loader purpose, `loaded` field, global loaders, parallel run and precedence order, escape-hatch caveat.
Removed: claims that Controls cannot edit loaded data and that `beforeEach` should be preferred; the page says neither.
Method: documentation only; no commands were run.
