---
id: computing-software.web-development.vitepress.code-blocks-shiki-highlighting
name: code-blocks-shiki-highlighting
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, shiki, syntax-highlighting, code-blocks, language-aliases, markdown-theme]
level: intro
status: docs-checked
description: "Highlight code blocks with Shiki by language alias, and configure theme, aliases and language labels in markdown options."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress uses Shiki for syntax highlighting. Add a valid language alias after the opening backticks:

````md
```js
export default { name: 'MyComponent' }
```

```html
<ul><li v-for="todo in todos" :key="todo.id">{{ todo.text }}</li></ul>
```
````

The supported language list is on the Shiki site. You can customize the highlight theme, configure language aliases and set custom language labels in the `markdown` option of site config (see the site config reference type declarations, which live in `src/node/markdown/markdown.ts`).

Related code-block features (each has its own skill): line highlighting `{4}`, `// [!code highlight]` comments, focus, diffs, errors and warnings, line numbers, snippets imported from files, and code groups.

To run Vue interpolation inside a fence, append `-vue` to the language, for example `js-vue` (see the escaping skill).

If a language label such as `c#` cannot be inferred from a file extension for imported snippets, specify it in braces.

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (Syntax Highlighting in Code Blocks, Unescape in Code Blocks via the using-vue guide, imported-snippet language in braces) and the site-config page (markdown option, link to src/node/markdown/markdown.ts). Removed: the unconfirmed claims that a language is needed for copy buttons and styling, the prompt-prefix convention, and the Verify step.

Method: documentation only; no commands were run.
