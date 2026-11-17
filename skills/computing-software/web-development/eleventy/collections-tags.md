---
id: computing-software.web-development.eleventy.collections-tags
name: collections-tags
category: computing-software
field: web-development
product: eleventy
tags: [collections, tags, collections-all, override-tags, eleventyexcludefromcollections]
level: intro
status: docs-checked
description: "Group Eleventy content into collections with front matter tags, use collections.all, exclude pages from collections and override inherited tags."
sources:
  - https://www.11ty.dev/docs/collections/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `tags` key has one purpose in Eleventy: building collections. A page can be in many collections.

```md
---
tags: post
---
```

Reference it in any template as `collections.post`. Several tags: `tags: ["cat", "dog"]` or a YAML list. A multi-word tag such as `tags: cat and dog` is read as `collections['cat and dog']`. Names containing `-` need square bracket notation in some template languages.

`collections.all` holds all content, tagged or not.

Exclude a page from every collection (including `all`) with `eleventyExcludeFromCollections: true`, useful for RSS feeds and sitemaps. In v3.0.0 and newer it can be an array of tag names, e.g. `["post"]`, to leave only those out.

Tags merge through the data cascade (deep merge), so tags set in directory data are combined with the page's own. To replace them:

```md
---
override:tags: []
---
```

For incremental builds (v2.0.0+), declare collections you use in data: `eleventyImport: { collections: ["post"] }`.

Mark the current page in a nav loop by comparing `post.url` with `page.url` and setting `aria-current="page"`.

## Checked

2026-11-04. Confirmed against the Eleventy Collections page: tags build collections, single and multiple tags, the multi-word tag form collections['cat and dog'], the dash-in-name bracket notation note, collections.all, eleventyExcludeFromCollections (boolean, array form from v3.0.0), deep-merged tags and the override:tags prefix, eleventyImport.collections (v2.0.0) and the aria-current comparison. Corrected the array-form version gate and the eleventyImport shape.

Method: documentation only; no commands were run.
