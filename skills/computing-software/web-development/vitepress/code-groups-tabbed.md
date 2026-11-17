---
id: computing-software.web-development.vitepress.code-groups-tabbed
name: code-groups-tabbed
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, code-group, code-tabs, tabbed-code, package-manager-tabs, snippet-in-code-group]
level: practitioner
status: docs-checked
description: "Show alternatives (npm/pnpm/yarn, JS/TS) as tabs with ::: code-group, titles in brackets, and imported snippets."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap fenced blocks in `::: code-group`; each block's tab label is the text in square brackets after the language.

````md
::: code-group

```sh [npm]
npm add -D vitepress
```

```sh [pnpm]
pnpm add -D vitepress
```

```ts [config.ts]
import type { UserConfig } from 'vitepress'
const config: UserConfig = {}
export default config
```

:::
````

**Imported snippets work too.** The filename is the default tab title, and you can supply your own after the highlight and attributes:

```md
::: code-group
<<< @/snippets/snippet.js
<<< @/snippets/snippet-with-region.js#snippet{1,2 ts:line-numbers} [snippet with region]
:::
```

**Nesting.** To mix code groups with other containers, make the outer container fence longer (`::::`) than the inner `:::` (see the nesting skill).

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (Code Groups, importing snippets in code groups, Nesting rule). Removed: the style tip about tab ordering and the claim about how the docs use it, and the Verify step. Thin skill: about 120 words survive; the id is kept.

Method: documentation only; no commands were run.
