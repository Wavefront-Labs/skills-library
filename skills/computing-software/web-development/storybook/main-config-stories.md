---
id: computing-software.web-development.storybook.main-config-stories
name: main-config-stories
category: computing-software
field: web-development
product: storybook
tags: [stories-glob, storiesspecifier, titleprefix, story-loading, picomatch]
level: practitioner
status: docs-checked
description: "Choose which story files load using globs or StoriesSpecifier objects with directory, files and titlePrefix."
sources:
  - https://storybook.js.org/docs/api/main-config/main-config-stories
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# main stories config

Goal: control where Storybook finds stories.

`stories` is required: an array of picomatch globs, or an async function receiving and returning the list. Default convention colocates `Button.stories.ts` next to `Button.ts`.

```ts
stories: [
  '../src/**/*.mdx',
  '../src/**/*.stories.@(js|jsx|ts|tsx)',
  {
    directory: '../packages/components',
    files: '**/*.stories.*',
    titlePrefix: 'Components',
  },
],
```

- Stories load in the order listed, which also orders the sidebar.
- A `StoriesSpecifier` is `{ directory: string; files?: string; titlePrefix?: string }`.
  - `directory` (required): where to start looking, relative to the project root.
  - `files`: glob relative to `directory` with no leading `./`; default `'**/*.@(mdx|stories.@(js|jsx|mjs|ts|tsx))'`.
  - `titlePrefix`: default `''`; the prefix used when auto-titling generates story titles.
- Change the naming convention with picomatch glob syntax, but some addons assume the default naming.
- A custom async implementation is allowed, but Storybook statically analyses the config for performance and custom logic may de-optimize or break that.

## Checked

Method: 2026-11-08 read docs/api/main-config/main-config-stories.mdx from the Storybook repo. Removed claims the page does not make (paths relative to main.ts, svelte extensions, experimental_indexers) and corrected the `directory` base and `files` default. The example block was not compared with the page snippet.
