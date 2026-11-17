---
id: computing-software.web-development.storybook.decorators-basics
name: decorators-basics
category: computing-software
field: web-development
product: storybook
tags: [decorators, decorator, story-wrapper, context-provider, wrap-story]
level: practitioner
status: docs-checked
description: "Wrap stories in extra markup or providers with decorators at story, component or global level."
sources:
  - https://storybook.js.org/docs/writing-stories/decorators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Decorators

Goal: give stories the layout or context they need without changing the stories.

A decorator wraps a story with extra rendering. Typical uses are spacing, theme providers and mocked context.

```tsx
const meta = preview.meta({
  component: Button,
  decorators: [
    (Story) => (
      <div style={{ margin: '3em' }}>
        <Story />
      </div>
    ),
  ],
});
```

Where to set them:
- Story: `decorators` on the story (keeps the story a pure rendering; the Source doc block works best this way).
- Component: `decorators` on the meta.
- Global: `decorators` in `definePreview` in `.storybook/preview.*`.

Framework notes:
- Angular: `componentWrapperDecorator(...)` from `@storybook/angular`.
- Vue: pass globals through `setup` so decorators stay reactive.
- Svelte: use a wrapper component and return `{ Component, props }` from the decorator.

Verify: the wrapper markup appears in the canvas.

## Checked
Date: 2026-11-04. Read the Decorators page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: levels, wrapper example, `componentWrapperDecorator` import, Vue and Svelte notes, Source block tip.
Removed: `moduleMetadata` (not on the page) and a sentence about providing data for connected components.
Method: documentation only; no commands were run.
