---
id: computing-software.web-development.docusaurus.code-npm2yarn-and-multilang
name: code-npm2yarn-and-multilang
category: computing-software
field: web-development
product: docusaurus
tags: [npm2yarn, remark-plugin, multi-language-tabs, codeblock-component, line-numbers]
level: practitioner
status: docs-checked
description: "Show line numbers, build multi-language code tabs, auto-convert npm commands with the npm2yarn remark plugin, and use CodeBlock in JSX."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-code-blocks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Line numbers: add `showLineNumbers` to the meta string; `showLineNumbers=3` starts counting at 3.

Multi-language tabs use the general `Tabs` component. Leave empty lines around each fenced block, a current MDX limitation:

````jsx
<Tabs>
<TabItem value="js" label="JavaScript">

```js
console.log('Hello');
```

</TabItem>
</Tabs>
````

Sync them with `groupId`.

npm2yarn shows CLI commands in several package managers. Install `@docusaurus/remark-plugin-npm2yarn`, register it in `remarkPlugins` of each content plugin that needs it:

```js title="docusaurus.config.js"
docs: {
  remarkPlugins: [[require('@docusaurus/remark-plugin-npm2yarn'), {sync: true}]],
},
blog: {
  remarkPlugins: [[require('@docusaurus/remark-plugin-npm2yarn'), {converters: ['pnpm']}]],
},
```

Options: `sync` (default `false`) syncs the choice across blocks; `converters` (default `'yarn'`, `'pnpm'`) where the first is the default choice. Then use the key:

````md
```bash npm2yarn
npm install @docusaurus/remark-plugin-npm2yarn
```
````

In JSX use `@theme/CodeBlock` with `language`, `title`, `showLineNumbers` and a string child. Highlighting only works for plain string children, and MDX turns line breaks inside `<pre>` into spaces, so write `{'\n'}` explicitly.

## Checked

2026-11-04. Read in full against the Docusaurus Code blocks page: showLineNumbers and showLineNumbers=3, Tabs for multi-language blocks with the empty-line MDX limitation, groupId syncing, npm2yarn registration and its options table (sync default false, converters default yarn and pnpm, first is the default), and CodeBlock in JSX with plain-string children and explicit newlines all match. Nothing removed.

Method: documentation only; no commands were run.
