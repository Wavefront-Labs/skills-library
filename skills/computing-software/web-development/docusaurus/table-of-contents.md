---
id: computing-software.web-development.docusaurus.table-of-contents
name: table-of-contents
category: computing-software
field: web-development
product: docusaurus
tags: [table-of-contents, toc-heading-levels, tocinline, toc-min-heading-level, hide-table-of-contents]
level: practitioner
status: docs-checked
description: "Control the page table of contents: heading level ranges per page or globally, inline TOC with TOCInline, filtering the toc array, and known generation edge cases."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-toc.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The top-right TOC shows h2 and h3 by default. Per page:

```md
---
toc_min_heading_level: 2
toc_max_heading_level: 5
---
```

Globally:

```js title="docusaurus.config.js"
themeConfig: {
  tableOfContents: {minHeadingLevel: 2, maxHeadingLevel: 5},
},
```

Front matter overrides the global setting but only affects the top-right TOC. The `themeConfig` option also applies to inline TOCs; each `<TOCInline />` otherwise uses its own `minHeadingLevel` and `maxHeadingLevel` props.

Inline TOC uses the `toc` global of any MDX document, a flat array of `{value, id, level}`:

```jsx
import TOCInline from '@theme/TOCInline';

<TOCInline
  toc={toc.filter((node) => node.level === 2 || node.level === 4)}
  minHeadingLevel={2}
  maxHeadingLevel={4}
/>
```

Generation is a Remark plugin with known false positives and negatives. Markdown headings inside hideable areas (`Tabs`, `details`) still appear. Non-Markdown headings (raw `<h2 id=...>`) do not appear in the TOC, which you can use to exclude a heading.

## Checked

2026-11-04. Read in full against the Docusaurus Headings and Table of contents page (markdown-features-toc.mdx): h2 and h3 default, toc_min_heading_level and toc_max_heading_level, themeConfig.tableOfContents, front matter scope, TOCInline props, the toc array shape and filtering, and the generation edge cases all match. Nothing removed.

Method: documentation only; no commands were run.
