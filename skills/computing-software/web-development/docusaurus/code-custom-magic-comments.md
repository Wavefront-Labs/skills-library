---
id: computing-software.web-development.docusaurus.code-custom-magic-comments
name: code-custom-magic-comments
category: computing-software
field: web-development
product: docusaurus
tags: [magiccomments, custom-directives, code-block-line, class-name, theme-config]
level: advanced
status: docs-checked
description: "Register custom magic comments in themeConfig.prism.magicComments, keep the default highlight entry first, style the class, and swizzle CodeBlock/Line."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-code-blocks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Magic comments such as `// highlight-next-line` are parsed and removed; they add metadata to the next line or to the block between a start and end comment.

Declare custom ones in `themeConfig.prism.magicComments`. Remember to repeat the default highlight entry:

```js title="docusaurus.config.js"
magicComments: [
  {
    className: 'theme-code-block-highlighted-line',
    line: 'highlight-next-line',
    block: {start: 'highlight-start', end: 'highlight-end'},
  },
  {
    className: 'code-block-error-line',
    line: 'This will error',
  },
],
```

Then a code block line `// This will error` precedes the line that gets the class. Style it:

```css
.code-block-error-line {
  background-color: #ff000020;
  display: block;
  margin: 0 calc(-1 * var(--ifm-pre-padding));
  padding: 0 var(--ifm-pre-padding);
  border-left: 3px solid #ff000080;
}
```

Each entry has `className` (required), plus `line` (applies to the directly following line) and/or `block` with `start` and `end`.

Metastring ranges like `{1,3-4}` apply the first `magicComments` entry's class, so changing the first entry changes their meaning. `magicComments: []` disables default highlight comments; a range with no entry at all is an error.

For markup control, swizzle `CodeBlock/Line`; it receives the list of class names.

## Checked

2026-11-04. Read in full against the Docusaurus Code blocks page, Custom magic comments section: themeConfig.prism.magicComments entry shape, repeating the default highlight entry, the error-line CSS, first-entry rule for metastring ranges, magicComments empty array, the error without any entry, and swizzling CodeBlock/Line all match. Nothing removed.

Method: documentation only; no commands were run.
