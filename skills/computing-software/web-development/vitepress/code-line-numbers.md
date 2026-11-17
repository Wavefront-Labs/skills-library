---
id: computing-software.web-development.vitepress.code-line-numbers
name: code-line-numbers
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, line-numbers, no-line-numbers, markdown-linenumbers, code-block-start-line]
level: intro
status: docs-checked
description: "Turn line numbers on globally with markdown.lineNumbers or per block with :line-numbers, :no-line-numbers and :line-numbers=2."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable globally in config:

```js
export default {
  markdown: { lineNumbers: true }
}
```

Override per block with a mark after the language:

````md
```ts {1}
// line numbers use the global default (off unless configured)
const line2 = 'This is line 2'
```

```ts:line-numbers {1}
// line numbers on
const line2 = 'This is line 2'
```

```ts:line-numbers=2 {1}
// line numbers on, first line numbered 2
const line3 = 'This is line 3'
```
````

- `:line-numbers` forces them on, `:no-line-numbers` forces them off.
- `:line-numbers=N` makes numbering start at N.
- Combine with line highlighting, as in `ts:line-numbers {1}`.
- For imported snippets the same marks go inside the braces: `<<< @/snippets/snippet.cs{1,2,4-6 c#:line-numbers}`.

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (Line Numbers and the imported-snippet braces form in Import Code Snippets). Removed: the claim about excerpts, the claim about where highlight ranges may appear relative to the colon mark, the tip about shell blocks, and the Verify step. Thin skill: about 120 words survive; the id is kept.

Method: documentation only; no commands were run.
