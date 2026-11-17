---
id: computing-software.web-development.storybook.naming-hierarchy-and-sorting
name: naming-hierarchy-and-sorting
category: computing-software
field: web-development
product: storybook
tags: [story-title, hierarchy, sorting, storysort, sidebar-order]
level: practitioner
status: docs-checked
description: "Place stories in the sidebar with title paths and order them with storySort, including nested order arrays."
sources:
  - https://storybook.js.org/docs/writing-stories/naming-components-and-hierarchy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Naming, grouping and sorting stories

Goal: organise the sidebar.

Set `title` in meta; use `/` to nest: `title: 'Design System/Atoms/Button'`. Hierarchy parts: category (root), folder, component, docs entry, story. Top-level groupings display as "root" items by default; this can be disabled in the sidebar configuration (see the sidebar-and-urls docs), though the page recommends naming components after the file hierarchy for large Storybooks. A single-story component (no siblings) whose display name exactly matches the last part of `title` is hoisted to replace its parent; story exports are start-cased (`myStory` becomes "My Story"), or override with `storyName`.

Sorting is import order by default. Add sorters to `storySorts` in `.storybook/main.ts`:

```ts
storySorts: [
  {
    order: ['Intro', 'Pages', ['Home', 'Login', 'Admin'], 'Components', '*', 'WIP'],
  },
],
```
- A sorter can be a function (it can use the story id, `title`, `name` and import path) or a configuration object with `method` (e.g. `'alphabetical'`), `order` (default `[]`), `includeNames` (default `false`) and `locales` (default system locale).
- `order`: names listed come first; stories matching no item come after the list; a nested array orders second-level items; `*` marks where all other stories go.
- `order` is independent of `method`: sort by `order`, then by method or default import order.
- With several sorters, each only orders stories the earlier ones consider equal.

## Checked

Method: 2026-11-08 read docs/writing-stories/naming-components-and-hierarchy.mdx and the page's storySorts snippet from the Storybook repo. Corrected the sort location (the page uses `storySorts` in main config, not `parameters.options.storySort`), removed the unsupported `sidebar.showRoots` key and a Verify step.
