---
id: computing-software.web-development.vitepress.escaping-vue-syntax-and-vue-code-blocks
name: escaping-vue-syntax-and-vue-code-blocks
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, v-pre, escape-interpolation, js-vue, code-block-vue, mustache-braces, literal-curly-braces]
level: practitioner
status: docs-checked
description: "Show literal {{ }} with v-pre spans or containers, and enable interpolation inside fences with the -vue suffix."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/using-vue.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since content is a Vue template, double curly braces are evaluated. To show them literally:

- Inline: wrap in an element with `v-pre`.

```md
This <span v-pre>{{ will be displayed as-is }}</span>
```

- Block: the `v-pre` custom container.

```md
::: v-pre
{{ This will be displayed as-is }}
:::
```

**Fenced code blocks are automatically wrapped in `v-pre`**, so no Vue syntax is processed inside them. To enable interpolation inside a fence, append `-vue` to the language, for example `js-vue`:

````md
```js-vue
Hello {{ 1 + 1 }}
```
````

Interpolation is evaluated inside that fence. The docs warn that this might prevent certain tokens from being highlighted properly.

Related: the Frontmatter docs also mention wrapping an expression in `v-pre` to display `$frontmatter` expressions literally.

## Checked

2026-11-04. Confirmed against the VitePress using-vue guide (Escaping, Unescape in Code Blocks) and the frontmatter guide (v-pre shows an expression literally). Removed: the unsupported remark about Vue, Handlebars and Jinja documentation, the literal 'Hello 2' output claim, and the Verify step. Thin skill: about 130 words survive; the id is kept.

Method: documentation only; no commands were run.
