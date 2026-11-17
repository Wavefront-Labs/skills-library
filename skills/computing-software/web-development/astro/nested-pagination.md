---
id: computing-software.web-development.astro.nested-pagination
name: nested-pagination
category: computing-software
field: web-development
product: astro
tags: [nested-pagination, tag-pages, paginate-params, flatmap]
level: advanced
status: docs-checked
description: "Combine pagination with another dynamic param, such as grouping posts by tag at /[tag]/[page], by returning one paginate() result per group."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nested pagination groups a paginated collection by a property or tag. Create `/src/pages/[tag]/[page].astro` to match `/red/1`, `/red/2`, `/blue/1`, `/green/1`.

Return an array of `paginate()` results from `getStaticPaths()`, one per grouping, and pass `{ params: { tag } }` to `paginate()` so Astro knows which grouping each result is for:

```astro title="src/pages/[tag]/[page].astro"
---
import type { GetStaticPaths } from "astro";

export const getStaticPaths = (({ paginate }) => {
  const allTags = ["red", "blue", "green"];
  const allPosts = Object.values(
    import.meta.glob("../pages/post/*.md", { eager: true }),
  );
  // For every tag, return a `paginate()` result.
  // Make sure that you pass `{ params: { tag }}` to `paginate()`
  // so that Astro knows which tag grouping the result is for.
  return allTags.flatMap((tag) => {
    const filteredPosts = allPosts.filter(
      (post: any) => post.frontmatter.tag === tag,
    );
    return paginate(filteredPosts, {
      params: { tag },
      pageSize: 10,
    });
  });
}) satisfies GetStaticPaths;

const { page } = Astro.props;
const params = Astro.params;
---
```

## Checked

2026-11-04. Confirmed against the Astro routing guide: the [tag]/[page] example and passing params to paginate(). Nothing removed.

Method: documentation only; no commands were run.
