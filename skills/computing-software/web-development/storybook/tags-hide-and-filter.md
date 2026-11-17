---
id: computing-software.web-development.storybook.tags-hide-and-filter
name: tags-hide-and-filter
category: computing-software
field: web-development
product: storybook
tags: [tags-hidefromsidebar, sidebar-filter, hide-stories, internal-stories, setfilter]
level: advanced
status: docs-checked
description: "Hide tagged stories from the sidebar, autodocs and filter menu, and add runtime filters from an addon."
sources:
  - https://storybook.js.org/docs/writing-stories/tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hiding stories and tags

Goal: keep internal or helper stories out of the UI.

Filtering by tag in the sidebar: choosing tags shows stories with any of them; Exclude hides stories with a tag; with nothing chosen all stories show. The filter is applied before search.

For stronger control, configure the tag in `.storybook/main.ts`:

```ts
tags: {
  internal: {
    hideFromSidebar: true,
    hideFromAutodocs: true,
    hideFromFilterPanel: true,
  },
},
```
- `hideFromSidebar` removes matching stories; clearing filters does not restore them.
- `hideFromAutodocs` removes them from autodocs pages.
- `hideFromFilterPanel` hides the tag from the filter menu but leaves stories visible.

Addons can register a runtime filter in the manager:

```ts
// .storybook/manager.ts
addons.register('internal-stories', (api) => {
  void api.setFilter('internal-stories', (item) => !item.tags?.includes('internal'));
});
```
A story or docs entry shows only when every registered filter passes. Register a filter that always returns true to stop filtering for that id.

Gotcha: `sidebar.filters` and `experimental_setFilter` were removed in Storybook 11.

## Checked

Method: 2026-11-08 read docs/writing-stories/tags.mdx from the Storybook repo; all claims and both code samples match the "Filtering the sidebar by tags" and "Hiding stories and tags" sections; removed an unsupported Verify step.
