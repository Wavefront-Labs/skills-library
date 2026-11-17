---
id: computing-software.web-development.docusaurus.mdx-remark-rehype-plugins
name: mdx-remark-rehype-plugins
category: computing-software
field: web-development
product: docusaurus
tags: [remark-plugins, rehype-plugins, mdx-plugins, esm-only-plugins, plugin-options]
level: advanced
status: docs-checked
description: "Install and configure remark and rehype plugins in Docusaurus content plugins, load ESM-only packages from CommonJS, and pass plugin options with tuples."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MDX transpiles Markdown to an AST (MDAST), then a Hypertext AST (HAST), then JSX. Remark plugins process the Markdown AST; rehype plugins process the Hypertext AST. Use them to reuse existing plugins, transform output of existing syntax, or add new syntax.

Docusaurus injects default remark plugins that generate the table of contents, add heading anchor links and transform images and links to `require()` calls.

Install the packages (for example `npm install --save remark-math rehype-katex`), then add them through the plugin or preset config (the example uses the docs options):

```js title="docusaurus.config.js"
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default {
  presets: [['@docusaurus/preset-classic', {
    docs: {
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    },
  }]],
};
```

Many official remark/rehype plugins are ES Modules only, so an ES Modules config file is recommended. In a CommonJS config use an async function with dynamic import: `remarkPlugins: [(await import('remark-math')).default]`.

Options use a tuple: `rehypePlugins: [[rehypeKatex, {strict: false}]]`. Check each plugin's docs for its options.

Default plugins run before custom ones, so images and links are already `require()` calls and the TOC does not see your changes. To run first, use `beforeDefaultRemarkPlugins` or `beforeDefaultRehypePlugins`.

## Checked

2026-11-04: read the Docusaurus MDX Plugins page in full. Confirmed MDAST and HAST, default plugins, install and config examples, the ESM-only advice with the dynamic import form, tuple options and the before-default options. Removed the claim that plugins are added to docs, blog and pages options, which the page does not state (it shows the docs options and says plugin or preset config).

Method: documentation only; no commands were run.
