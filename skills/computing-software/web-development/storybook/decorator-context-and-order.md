---
id: computing-software.web-development.storybook.decorator-context-and-order
name: decorator-context-and-order
category: computing-software
field: web-development
product: storybook
tags: [decorator-context, story-context, decorator-order, globals-in-decorators, hooks]
level: advanced
status: docs-checked
description: "Use the story context argument in decorators and know the execution order across global, component and story levels."
sources:
  - https://storybook.js.org/docs/writing-stories/decorators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Decorator context and ordering

Goal: make decorators react to args, globals and parameters, and predict their order.

The second argument of a decorator is the story context:
- `args`: story args
- `argTypes`: only in decorators and render functions (not in loaders, `beforeEach`, `play`, `afterEach`)
- `globals`: Storybook-wide globals (for example from toolbars)
- `hooks`: Storybook hooks
- `parameters`: static story metadata
- `viewMode`: the current view mode (for example canvas or docs)

```tsx
export const withLayout = (Story, context) => {
  const Layout = context.parameters.pageLayout === 'page' ? PageLayout : Fragment;
  return <Layout><Story /></Layout>;
};
```

Order once a story renders: global decorators in the order defined, then component decorators, then story decorators (story decorators start from the innermost and work outwards).

In Vue, pass globals through the `setup` function and use `computed` for derived values so they stay reactive.

Verify: changing the toolbar global or story parameter changes the wrapper without editing the story.

## Checked
Date: 2026-11-04. Read the Decorators page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: context properties, `argTypes` restriction, execution order, Vue guidance.
Fixed: softened `viewMode` to "for example canvas or docs". Removed the theme-switching tip, which the page does not give.
Method: documentation only; no commands were run.
