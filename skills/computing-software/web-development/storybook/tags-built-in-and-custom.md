---
id: computing-software.web-development.storybook.tags-built-in-and-custom
name: tags-built-in-and-custom
category: computing-software
field: web-development
product: storybook
tags: [tags, built-in-tags, custom-tags, dev-tag, test-tag]
level: practitioner
status: docs-checked
description: "Use built-in tags (dev, manifest, test, autodocs, play-fn) and define custom tags with sidebar filter defaults."
sources:
  - https://storybook.js.org/docs/writing-stories/tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tags

Goal: include, exclude and categorise stories without moving files.

Built-in tags:
- `dev` (default): shown in the sidebar
- `manifest` (default): included in component and docs manifests
- `test` (default): run by the Vitest addon
- `autodocs` (not default): story is included in the docs page; a file with none gets no docs page
- `play-fn`: added automatically to stories with a play function
- `test-fn`: added to tests made with the experimental `.test` method

Apply an array of static strings at project, meta or story level:

```ts
export const Edge = meta.story({ tags: ['experimental', '!test'] });
```
Prefix with `!` to remove a tag (also at project or meta level).

Define custom tags in `main.ts` for filter defaults:
```ts
tags: { experimental: { defaultFilterSelection: 'exclude' } },
```
`include` preselects the tag in the sidebar filter; `exclude` hides those stories until included.

Built-in and custom tags both appear in the sidebar filter menu. `dev`, `manifest` and `test` are applied implicitly to every story.

Recipes on the page: a docs-only story enables `autodocs` and removes `dev`; a grid "combo" story of variants can be kept out of testing with tags while the variants are still tested individually; the experimental `_test` tag can be excluded from the sidebar by default via `main.ts`.

## Checked

Method: 2026-11-08 read docs/writing-stories/tags.mdx from the Storybook repo; kept the tag table, `!` removal and `defaultFilterSelection`; dropped an "expected error" recipe the page does not state and an unsupported Verify step. The `!test` code line is an illustration consistent with the removal rule, not a copied snippet.
