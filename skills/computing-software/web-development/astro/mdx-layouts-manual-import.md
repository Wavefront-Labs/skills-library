---
id: computing-software.web-development.astro.mdx-layouts-manual-import
name: mdx-layouts-manual-import
category: computing-software
field: web-development
product: astro
tags: [mdx, mdx-layout, manual-layout-import, meta-charset]
level: advanced
status: docs-checked
description: "Pass extra values to a layout from an MDX page by importing and using a Layout component instead of the layout frontmatter property, and keep meta charset."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/layouts.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `layout` frontmatter property also works in MDX and passes `frontmatter` and `headings`. To pass information that does not (or cannot) exist in frontmatter, import and use a `<Layout />` component instead. It receives no props automatically; pass what it needs:

```mdx title="src/pages/posts/first-post.mdx"
---
title: 'My first MDX post'
publishDate: '21 September 2022'
---
import BaseLayout from '../../layouts/BaseLayout.astro';

export function fancyJsHelper() {
  return "Try doing that with YAML!";
}

<BaseLayout title={frontmatter.title} fancyJsHelper={fancyJsHelper}>
  Welcome to my new Astro blog, using MDX!
</BaseLayout>
```

The layout reads them from `Astro.props`, and MDX content goes where `<slot />` is:

```astro title="src/layouts/BaseLayout.astro"
---
const { title, fancyJsHelper } = Astro.props;
---
<html>
  <head>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>{title}</h1>
    <slot />
    <p>{fancyJsHelper()}</p>
  </body>
</html>
```

With any layout (frontmatter property or import), include `<meta charset="utf-8">` in the layout; Astro no longer adds it automatically to MDX pages. Remove the `layout` frontmatter line when importing manually.

## Checked

2026-11-04. Confirmed against the Astro layouts page: layout frontmatter in MDX, manual Layout import with explicit props, meta charset requirement; the removed layout line follows the page's example diff markup. Nothing removed.

Method: documentation only; no commands were run.
