---
id: computing-software.web-development.storybook.stories-for-multiple-components
name: stories-for-multiple-components
category: computing-software
field: web-development
product: storybook
tags: [subcomponents, multiple-components, template-component, children-arg, composite-stories]
level: practitioner
status: docs-checked
description: "Document parent and child components together with subcomponents and reuse story definitions."
sources:
  - https://storybook.js.org/docs/writing-stories/stories-for-multiple-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stories for multiple components

Goal: write stories for components that work together (List and ListItem).

`subcomponents` in meta adds an extra tab in the ArgTypes and Controls tables for each child:

```ts
const meta = preview.meta({
  component: List,
  subcomponents: { ListItem },
});
```
Limits: subcomponent argTypes are inferred only (cannot be overridden) and their tables have no controls, since controls apply only to the main component's args.

Better reuse options:
1. Reuse story args: render `ListItem` stories' args inside the List story.
2. Make `children` an arg and compose stories. Args must be JSON serializable: avoid empty values, use `mapping` if you want Controls to switch it, and be careful with third-party components.
3. A template component, a story-generating component that takes data args, so Controls can alter them.

Choose subcomponents for documentation only and args-based composition when you also need interactivity.

The docs describe the extra panel as listing the props of `ListItem`. Args-based `children` reuse is shown for React; the page says children-arg editing in Controls is still being improved.

## Checked

Method: 2026-11-08 read docs/writing-stories/stories-for-multiple-components.mdx from the Storybook repo. Claims match; reworded the subcomponent panel and React scope, removed an unsupported Verify step. Code samples were not compared with the page snippets.
