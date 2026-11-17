---
id: computing-software.web-development.astro.pagination-paginate
name: pagination-paginate
category: computing-software
field: web-development
product: astro
tags: [pagination, paginate, page-prop, page-size]
level: practitioner
status: docs-checked
description: "Split a collection across pages with paginate() in getStaticPaths and build navigation from the page prop: currentPage, data, and url.prev/next/first/last."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Name the file with a bracket param, e.g. `/astronauts/[page].astro`, and call `paginate()` from `getStaticPaths`:

```astro title="src/pages/astronauts/[page].astro"
---
import type { GetStaticPaths } from "astro";

export const getStaticPaths = (({ paginate }) => {
  const astronautPages = [
    { astronaut: "Neil Armstrong" },
    { astronaut: "Buzz Aldrin" },
    { astronaut: "Sally Ride" },
    { astronaut: "John Glenn" },
  ];

  // Generate pages from our array of astronauts, with 2 to a page
  return paginate(astronautPages, { pageSize: 2 });
}) satisfies GetStaticPaths;

// All paginated data is passed on the "page" prop
const { page } = Astro.props;
---
<h1>Page {page.currentPage}</h1>
<ul>
  {page.data.map(({ astronaut }) => <li>{astronaut}</li>)}
</ul>
```

This generates `/astronauts/1` and `/astronauts/2`.

The `page` prop has `data`, `start`, `end`, `total`, `currentPage`, `size` (default: 10), `lastPage`, and `url` with `current`, `prev`, `next`, `first`, `last` (each may be undefined). Build navigation from them:

```astro
{page.url.first ? <a href={page.url.first}>First</a> : null}
{page.url.prev ? <a href={page.url.prev}>Previous</a> : null}
{page.url.next ? <a href={page.url.next}>Next</a> : null}
{page.url.last ? <a href={page.url.last}>Last</a> : null}
```

## Checked

2026-11-04. Confirmed against the Astro routing guide: paginate() usage, the page prop fields, size default 10 and the url fields. Nothing removed.

Method: documentation only; no commands were run.
