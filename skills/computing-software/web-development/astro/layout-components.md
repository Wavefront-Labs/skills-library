---
id: computing-software.web-development.astro.layout-components
name: layout-components
category: computing-software
field: web-development
product: astro
tags: [layouts, page-shell, slot, typed-layout-props]
level: intro
status: docs-checked
description: "Build an Astro layout component with a page shell and slot, type its props, and nest layouts such as a post layout inside a base layout."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/layouts.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A layout is an ordinary Astro component providing a page shell (`<html>`, `<head>`, `<body>`) and a `<slot />` for page content. If it has a shell, `<html>` must be the parent of all other elements. Placing them in `src/layouts` is a convention; prefix names with `_` to colocate with pages.

```astro
---
// src/layouts/MySiteLayout.astro
import BaseHead from '../components/BaseHead.astro';
const { title } = Astro.props;
---
<html lang="en">
  <head>
    <meta charset="utf-8">
    <BaseHead title={title}/>
  </head>
  <body>
    <h1>{title}</h1>
    <article>
      <slot /> <!-- your content is injected here -->
    </article>
  </body>
</html>
```

```astro title="src/pages/index.astro"
---
import MySiteLayout from '../layouts/MySiteLayout.astro';
---
<MySiteLayout title="Home Page">
  <p>My page content, wrapped in a layout!</p>
</MySiteLayout>
```

Add types with a `Props` interface:

```astro
---
interface Props { 
  title: string;
  description: string;
}
const { title, description } = Astro.props;
---
```

Nest layouts by wrapping one in another and passing props along:

```astro
---
// src/layouts/BlogPostLayout.astro
import BaseLayout from './BaseLayout.astro';
const { frontmatter } = Astro.props;
---
<BaseLayout url={frontmatter.url}>
  <h1>{frontmatter.title}</h1>
  <slot />
</BaseLayout>
```

## Checked

2026-11-04. Confirmed against the Astro layouts page: page shell and slot, html as parent rule, src/layouts convention and underscore prefix, Props typing, nesting layouts. Nothing removed.

Method: documentation only; no commands were run.
