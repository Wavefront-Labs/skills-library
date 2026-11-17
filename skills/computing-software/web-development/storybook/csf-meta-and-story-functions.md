---
id: computing-software.web-development.storybook.csf-meta-and-story-functions
name: csf-meta-and-story-functions
category: computing-software
field: web-development
product: storybook
tags: [meta-story, preview-meta, meta-type, story-function, csf-api]
level: practitioner
status: docs-checked
description: "Define meta with preview.meta and stories with meta.story, and add custom arg types with type helpers."
sources:
  - https://storybook.js.org/docs/writing-stories/csf/api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# preview.meta and meta.story

Goal: define a component's metadata and stories with full typing.

`preview.meta(annotations)` takes `component`, an optional `title`, and shared annotations. `title` must be unique; if omitted it is inferred from the file path. It returns a meta object whose `story()` method defines stories.

```ts
const meta = preview.meta({
  component: List,
  title: 'Lists/List',
  args: { items: [] },
});

export const Empty = meta.story();
export const Full = meta.story({ args: { items: ['a', 'b'] } });
```

Args set in meta must be real args of the story (component props, for example).

Custom args: use `preview.type<{ args: CustomArgs }>().meta({...})` for args shared by the whole file, and `meta.type<{ args: { icon?: string } }>().story({...})` for one story.

In Svelte CSF, the meta's `Story` component defines stories. A `.stories.svelte` file compiles to CSF 4.

Verify: a mistyped arg value (for example `variant: 'primry'`) shows a TypeScript error.

## Checked
Date: 2026-11-04. Read the CSF 4 API page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: `title` rules, `meta.story()`, args-must-be-real rule, the two type helpers, Svelte behavior.
Fixed: the type helpers are now shown in their real call forms. Removed the claim that an extra story arg must be set in that story.
Method: documentation only; no commands were run.
