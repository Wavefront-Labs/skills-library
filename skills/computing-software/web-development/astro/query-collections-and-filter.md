---
id: computing-software.web-development.astro.query-collections-and-filter
name: query-collections-and-filter
category: computing-software
field: web-development
product: astro
tags: [getcollection, getentry, filter-collection, sort-order, draft-posts]
level: practitioner
status: docs-checked
description: "Query build-time collections with getCollection and getEntry, sort entries yourself, filter drafts or subdirectories, and type entries as props."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`getCollection()` returns an array of entries; `getEntry()` one entry. Entries have an `id`, a `data` object, and a `body` with the raw body of Markdown, MDX or Markdoc.

```astro
---
import { getCollection, getEntry } from 'astro:content';

const allBlogPosts = await getCollection('blog');
const poodleData = await getEntry('dogs', 'poodle');
---
```

Order is non-deterministic and platform-dependent, so sort yourself:

```astro
const posts = (await getCollection('blog')).sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
);
```

A filter callback receives `id` and `data`. Hide drafts only in production:

```astro
const blogEntries = await getCollection('blog', ({ data }) => {
  return import.meta.env.PROD ? data.draft !== true : true;
});
```

Filter by nested directory (the `id` includes the path):

```astro
const englishDocsEntries = await getCollection('docs', ({ id }) => {
  return id.startsWith('en/');
});
```

Type a prop with `CollectionEntry`:

```astro
---
import type { CollectionEntry } from 'astro:content';
interface Props {
  post: CollectionEntry<'blog'>;
}
const { post } = Astro.props;
---
```

## Checked

2026-11-04. Confirmed against the Astro content collections guide: getCollection and getEntry, non-deterministic sort order, filter callbacks, id-prefix filtering and CollectionEntry typing. Nothing removed.

Method: documentation only; no commands were run.
