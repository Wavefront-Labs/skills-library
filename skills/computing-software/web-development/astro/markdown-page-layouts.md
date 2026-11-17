---
id: computing-software.web-development.astro.markdown-page-layouts
name: markdown-page-layouts
category: computing-software
field: web-development
product: astro
tags: [markdown-layout, frontmatter-prop, markdownlayoutprops, headings]
level: practitioner
status: docs-checked
description: "Wrap Markdown pages in an Astro layout via the layout frontmatter property, read frontmatter and headings from Astro.props, and type them with MarkdownLayoutProps."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/layouts.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For `.md` files in `src/pages/`, the `layout` frontmatter property names the `.astro` layout. It is not special when using content collections. All frontmatter properties arrive as props.

```markdown title="src/pages/page.md"
---
layout: ../layouts/BlogPostLayout.astro
title: "Hello, World!"
author: "Matthew Phillips"
---
```

```astro title="src/layouts/BlogPostLayout.astro"
---
const { frontmatter } = Astro.props;
---
<html>
  <head>
    <meta charset="utf-8">
    <title>{frontmatter.title}</title>
  </head>
  <body>
    <h1>{frontmatter.title} by {frontmatter.author}</h1>
    <slot />
  </body>
</html>
```

Type it with `MarkdownLayoutProps`:

```astro
---
import type { MarkdownLayoutProps } from 'astro';

type Props = MarkdownLayoutProps<{
  title: string;
  author: string;
}>;

const { frontmatter, url } = Astro.props;
---
```

Props available via `Astro.props`: `file`, `url`, `frontmatter` (also with nested `file` and `url`), `headings` (`{ depth: number; slug: string; text: string }[]`), `rawContent()` and async `compiledContent()`. Headings are an array here, not a `getHeadings()` function.

## Checked

2026-11-04. Confirmed against the Astro layouts page: layout frontmatter for .md files in src/pages, not special in content collections, frontmatter prop, MarkdownLayoutProps, the list of Astro.props fields and headings type. Nothing removed.

Method: documentation only; no commands were run.
