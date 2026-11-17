---
id: computing-software.web-development.eleventy.pagination-objects-and-permalinks
name: pagination-objects-and-permalinks
category: computing-software
field: web-development
product: eleventy
tags: [pagination-object, resolve-values, pagination-permalink, pagenumber, addallpagestocollections]
level: practitioner
status: docs-checked
description: "Paginate objects by keys or values, build paginated permalinks from pageNumber or item data, and add every pagination page to collections."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/pagination.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Paging an object.** Objects resolve with `Object.keys` by default, so `pagination.items[0]` holds a key (`["itemkey1"]`); read the value with `testdata[ pagination.items[0] ]`. For values add `resolve: values`.

```yaml
pagination:
  data: testdata
  size: 1
  resolve: values
```

**Permalinks** support template syntax with pagination variables:

```yaml
permalink: "different/page-{{ pagination.pageNumber }}/index.html"
```

Nunjucks can start at 1 with `pagination.pageNumber + 1`; Liquid needs `pagination.pageNumber | plus: 1`. Logic works too, e.g. `{% if pagination.pageNumber > 0 %}page-{{ pagination.pageNumber + 1 }}/{% endif %}` to keep page one at the base URL.

Use item data: `permalink: "different/{{ pagination.items[0] | slugify }}/index.html"` writes `different/my-item/index.html` for `My Item`.

**Tags on paginated templates.** By default only the first page enters the collections for the template's `tags`. Set `addAllPagesToCollections: true` (0.8.0+) in `pagination` to add every page.

**Option list (the page's full list):** `data`, `size` (required), `alias`, `generatePageOnEmptyData`, `resolve: values`, `filter`, `reverse`, `addAllPagesToCollections`. The `before` callback is documented separately in the page's data-modification section.

## Checked

2026-11-08. Confirmed against the Eleventy docs Pagination page (markdown source): object paging with keys and `resolve: values`, permalink templating with `pageNumber`, the Nunjucks versus Liquid increment note, item-based permalinks, and `addAllPagesToCollections`. Removed the "see the tag-pages skill" pointer, which the page does not state (it links a Quick Tip instead), and moved `before` out of the option list because the page's list omits it.

Method: documentation only; no commands were run.
