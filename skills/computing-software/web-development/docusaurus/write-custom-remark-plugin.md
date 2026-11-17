---
id: computing-software.web-development.docusaurus.write-custom-remark-plugin
name: write-custom-remark-plugin
category: computing-software
field: web-development
product: docusaurus
tags: [custom-remark-plugin, unist-util-visit, transformer, vfile, before-default-plugins]
level: advanced
status: docs-checked
description: "Write your own remark plugin for Docusaurus Markdown: the options-to-transformer shape, visiting headings, reading the vfile path, and plugin ordering."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A remark or rehype plugin is a function that receives `options` and returns a `transformer` operating on the AST. Put it anywhere, for example `src/remark/section-prefix.js` (or publish it as an npm package).

This one prefixes every h2 with `Section X. `:

```js title="src/remark/section-prefix.js"
import {visit} from 'unist-util-visit';

const plugin = (options) => {
  const transformer = async (ast) => {
    let number = 1;
    visit(ast, 'heading', (node) => {
      if (node.depth === 2 && node.children.length > 0) {
        node.children.unshift({type: 'text', value: `Section ${number}. `});
        number++;
      }
    });
  };
  return transformer;
};

export default plugin;
```

Import it in the config and register it like an installed plugin:

```js title="docusaurus.config.js"
import sectionPrefix from './src/remark/section-prefix';

docs: {remarkPlugins: [sectionPrefix]},
```

The transformer's second parameter is a `vfile`, useful for the current Markdown file path (`vfile.path`). Docusaurus's own `transformImage` plugin uses it to convert relative image references to `require()` calls.

Default Docusaurus plugins run before your remark plugins, so the generated TOC does not show the prefix. Register under `beforeDefaultRemarkPlugins` for the TOC to include it.

## Checked

2026-11-04: read the Docusaurus MDX Plugins page in full. Confirmed the options-to-transformer shape, the section-prefix example, registration, the vfile second parameter, transformImage, and default plugin ordering with beforeDefaultRemarkPlugins. Nothing removed.

Method: documentation only; no commands were run.
