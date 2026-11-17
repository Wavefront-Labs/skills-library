---
id: computing-software.web-development.ghost.ghost-routes-yaml-collections-and-taxonomies
name: ghost-routes-yaml-collections-and-taxonomies
category: computing-software
field: web-development
product: ghost
tags: [ghost, routes-yaml, collections, taxonomies, permalink, filter, multilingual]
level: advanced
status: docs-checked
description: "Configure Ghost collections with permalinks and NQL filters, order filters correctly, and keep tag and author taxonomies defined."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/routing.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/filter-property-routes-yaml.mdx
  - https://github.com/TryGhost/docs/blob/main/faq/url-for-tags-and-authors-returns-404.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split a site into sections such as /blog/ and /podcast/.

Collections determine both the index route that lists posts and the URL structure of posts. A post can belong to only one collection.

```yaml
routes:
  /: home
collections:
  /blog/:
    permalink: /blog/{slug}/
    template: blog
    filter: primary_tag:blog
  /podcast/:
    permalink: /podcast/{slug}/
    template: podcast
    filter: primary_tag:podcast
```
`primary_tag` is the first tag in the editor, which keeps it unique. A collection `data:` value (for example `data: tag.work`) passes that tag's data into the index and redirects the tag URL.

Rules:
- Keep filters unique from one another; matching several collections can cause problems with post rendering and collection pagination.
- Specify inverse filters with `-` so pagination is correct, e.g. `/es/` uses `tag:es`, `/fr/` uses `tag:fr` and the generic `/` uses `tag:-[fr,es]` (the FAQ describes this as needed in the "current beta version" of dynamic routing).
- A post lives in the first collection where it matches the filter, so put generic filters towards the end.
- Multi-language sites: the page's example uses a private tag `#de` with filters `'tag:-hash-de'` on `/` and `'tag:hash-de'` on `/de/`; private tags are not shown on the front end.
- Routes need trailing slashes for dynamic routing to function correctly. The `order` property defaults to `published_at desc`.

Taxonomies: `tag` and `author` must stay present or individual tag and author URLs return 404; their permalinks can be changed (for example `tag: /topic/{slug}/`). You cannot define new taxonomies. Leaving `taxonomies:` empty removes the archives, so update templates that link to them. Unlike collections, posts can appear in several taxonomies.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, no imported snippets): themes/routing.mdx (445 lines), faq/filter-property-routes-yaml.mdx (29 lines), faq/url-for-tags-and-authors-returns-404.mdx (14 lines). Changed: the example's blog template to `blog` as on the page. Reworded the "overlaps break" and multi-language statements to the page's wording. Removed the Verify step. Added taxonomy customisation, trailing-slash and order details.
Method: documentation only; no commands were run.
