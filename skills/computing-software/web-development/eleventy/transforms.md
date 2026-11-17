---
id: computing-software.web-development.eleventy.transforms
name: transforms
category: computing-software
field: web-development
product: eleventy
tags: [transforms, addtransform, html-minify, postprocess, rendertransforms]
level: practitioner
status: docs-checked
description: "Post-process Eleventy output with addTransform: required return value, this.page access, execution order, plugin ordering and an HTML minify example."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/transforms.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A transform modifies a template's output (for example to prettify or minify HTML). It can be sync or async and **must return** the original or transformed content.

```js
eleventyConfig.addTransform("transform-name", async function (content) {
  console.log(this.page.inputPath);
  // Caution: outputPath could be `false` (from permalink)
  console.log(this.page.outputPath);
  return content;
});
```

`this.page` is available from v2.0.

**Order:** transforms run in order of insertion. Transforms added inside a plugin are inserted in the plugin's second configuration stage, so they run after the transforms in the main config:

```js
eleventyConfig.addPlugin((eleventyConfig) => {
  eleventyConfig.addTransform("third", () => {});
});
eleventyConfig.addTransform("first", () => {});
eleventyConfig.addTransform("second", () => {});
```

**Run manually** (3.0.0-alpha.11+): the `renderTransforms` universal filter applies transforms to blocks of arbitrary HTML.

**Minify example** using `html-minifier-terser`:

```js
eleventyConfig.addTransform("htmlmin", function (content) {
  if ((this.page.outputPath || "").endsWith(".html")) {
    return htmlmin.minify(content, { useShortDoctype: true, removeComments: true, collapseWhitespace: true });
  }
  return content;
});
```

The `|| ""` guards against `permalink: false`. Return non-HTML output unchanged.

## Checked

2026-11-08. Confirmed against the Eleventy docs Transforms page (markdown source): the must-return rule, sync or async callbacks, this.page from v2.0, the outputPath false caution, insertion order, plugin second-stage ordering, renderTransforms (3.0.0-alpha.11) and the htmlmin example. Nothing removed.

Method: documentation only; no commands were run.
