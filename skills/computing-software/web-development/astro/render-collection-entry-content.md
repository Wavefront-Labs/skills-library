---
id: computing-software.web-development.astro.render-collection-entry-content
name: render-collection-entry-content
category: computing-software
field: web-development
product: astro
tags: [render-function, content-component, collection-entry, mdx-content]
level: intro
status: docs-checked
description: "Render a Markdown or MDX collection entry to HTML with render() from astro:content and place its Content component in a page."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `render()` from `astro:content` on a queried Markdown or MDX entry. It gives you a `<Content />` component and the list of rendered headings.

```astro title="src/pages/blog/post-1.astro"
---
import { getEntry, render } from "astro:content";

const entry = await getEntry("blog", "post-1");

if (!entry) {
  throw new Error("Entry not found");
}

const { Content } = await render(entry);
---

<h1>{entry.data.title}</h1>
<p>Published on: {entry.data.pubDate.toDateString()}</p>
<Content />
```

Display metadata from `data`, e.g. a post list:

```astro
<ul>
  {posts.map(post => (
    <li><a href={`/blog/${post.id}`}>{post.data.title}</a></li>
  ))}
</ul>
```

For MDX entries you can pass your own components to `<Content />` to replace HTML elements.

## Checked

2026-11-04. Confirmed against the Astro content collections guide: render() from astro:content, the Content component, headings, and passing components for MDX. Nothing removed.

Method: documentation only; no commands were run.
