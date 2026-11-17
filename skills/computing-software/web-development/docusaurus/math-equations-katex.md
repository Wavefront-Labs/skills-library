---
id: computing-software.web-development.docusaurus.math-equations-katex
name: math-equations-katex
category: computing-software
field: web-development
product: docusaurus
tags: [katex, math-equations, remark-math, rehype-katex, latex]
level: practitioner
status: docs-checked
description: "Enable KaTeX math in Docusaurus: install remark-math and rehype-katex, register them, add the KaTeX stylesheet, write inline and block equations, self-host assets."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-math-equations.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Writing: inline math is wrapped in `$`. Display (block) math uses a fenced code block with `math`:

````latex
Let $F(x)=\int_{a}^{x} f(t)\,dt$.

```math
I = \int_0^{2\pi} \sin(x)\,dx
```
````

`$$` fences also work but rely on a Markdown syntax extension and are less portable.

Enable:

1. Install `remark-math@6` and `rehype-katex@7`. Use these versions: they are compatible with the MDX v3 that Docusaurus uses, and other versions are not guaranteed.
2. Both are ES Modules only, so an ES Modules config file is recommended (a CommonJS config can use an async config creator function with dynamic imports):

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

3. Include the KaTeX CSS under `stylesheets` (a `href` for `katex.min.css`, with `type: 'text/css'`, plus the integrity and `crossorigin` values from the KaTeX CDN).

Self-hosting: download a KaTeX release, copy `katex.min.css` and the `fonts` directory (`.woff2` should suffice) into `static`, and point the stylesheet `href` to a local path such as `/katex/katex.min.css`.

## Checked

2026-11-04. Read in full against the Docusaurus Math Equations page (markdown-features-math-equations.mdx): inline $ and math fences, $$ portability note, remark-math 6 and rehype-katex 7 for MDX v3, ES Modules config, the stylesheets entry and self-hosting steps match. Removed the unstated claim that the plugins must be applied to every content plugin, and softened the ES Modules wording to match the page (recommended, with an async config creator for CommonJS).

Method: documentation only; no commands were run.
