---
id: computing-software.web-development.storybook.args-levels
name: args-levels
category: computing-software
field: web-development
product: storybook
tags: [args, story-args, component-args, global-args, arg-reuse]
level: intro
status: docs-checked
description: "Define args at story, component and global level and compose them across stories."
sources:
  - https://storybook.js.org/docs/writing-stories/args
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Args at every level

Goal: set component inputs once and reuse them.

Args are a JSON-serializable object of string keys that Storybook passes to the component (props, slots, inputs). When an arg changes the component re-renders, which is how Controls and other addons edit stories live. You do not change component code.

- Story level: `args` on the story.
- Component level: `args` in the meta; applies to all stories of the file unless overridden.
- Global level: `args` in `definePreview` in `.storybook/preview.*`; applies to every story.

```ts
export const Primary = meta.story({ args: { primary: true, label: 'Button' } });
export const PrimaryLong = Primary.extend({ args: { label: 'A very long label' } });
```

Compose with object spread or, in CSF 4, with `Story.extend`. For composite components, reuse the child stories' args inside the parent's args.

Guidance:
- If most stories repeat the same args, move them to meta.
- For settings applied everywhere (a theme), prefer globals with a toolbar over global args.
- Args can set anything the component accepts, such as a `footer` arg that populates a child.

Verify: change an arg in the Controls panel and the canvas re-renders.

## Checked
Date: 2026-11-04. Read the Args page and the CSF 4 API page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: three levels, JSON-serializable, composition, globals preferred for themes, `Story.extend`.
Method: documentation only; no commands were run.
