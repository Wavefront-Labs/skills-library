---
id: computing-software.web-development.storybook.csf-story-names-and-exports
name: csf-story-names-and-exports
category: computing-software
field: web-development
product: storybook
tags: [story-names, start-case, includestories, excludestories, non-story-exports]
level: practitioner
status: docs-checked
description: "Control story display names and ids, and mix stories with non-story exports using includeStories and excludeStories."
sources:
  - https://storybook.js.org/docs/writing-stories/csf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Story names and non-story exports

Goal: predictable sidebar names and clean story files.

Display names come from the export identifier converted to start case:

| Identifier | Name |
| --- | --- |
| someName | Some Name |
| someNAME | Some NAME |
| some_custom_NAME | Some Custom NAME |
| someName1234 | Some Name 1 2 3 4 |

Start export names with a capital letter. Override with the `name` property when you need reserved words, emoji or different spacing, or to keep the story id stable while changing the label (stable ids help third-party tools).

Non-story exports (for example mock data) are controlled in meta with `includeStories` / `excludeStories`, as arrays of strings or regular expressions:

```ts
const meta = preview.meta({
  component: List,
  excludeStories: /.*Data$/,
});
export const simpleData = [1, 2];       // ignored
export const Simple = meta.story({});   // a story
```

Equivalent options: `includeStories: /^[A-Z]/` (recommended with UpperCamelCase), `includeStories: ['Simple', 'Complex']`, `excludeStories: ['simpleData']`.

Verify: only the intended exports appear in the sidebar.

## Checked
Date: 2026-11-04. Read the CSF page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: start-case table, `name` override, `includeStories` and `excludeStories` forms and the recommended regex.
Method: documentation only; no commands were run.
