---
id: computing-software.web-development.eleventy.pagination-basics
name: pagination-basics
category: computing-software
field: web-development
product: eleventy
tags: [pagination, pagination-size, pagination-items, pagination-href, paging-array]
level: intro
status: docs-checked
description: "Create multiple Eleventy output pages from one template with the pagination front matter key, and read the pagination object for items and links."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/pagination.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add `pagination` to front matter with `data` (a Lodash get path to the data set) and `size` (required). Each output page gets one chunk.

```yaml
---
pagination:
  data: testdata
  size: 2
testdata: [item1, item2, item3, item4]
---
```

If the file is `paged.njk`, this writes `_site/paged/index.html` and `_site/paged/1/index.html`.

The `pagination` object holds:

- `items`: current chunk; `pageNumber`: 0 indexed
- `hrefs`: all page hrefs in order; `href.next`, `href.previous`, `href.first`, `href.last`
- `pages`: all chunks in order; `page.next`, `page.previous`, `page.first`, `page.last`

Use `<a href="{{ pagination.href.next }}">Next Page</a>`. Older names (`nextPageHref`, `links`, `pageLinks`) remain for backwards compatibility; prefer `href.*` and `hrefs`.

`data` may point at front matter, global data or a local data file (e.g. `myData` from `_data/globalDataSet.json`), or a collection such as `collections.post`.

Alias `pagination.items[0]` to a nicer name with `alias: item`. With `size` above 1 the alias is an array. `page` is reserved; you cannot use `alias: page`.

By default an empty data set renders no pages; `generatePageOnEmptyData: true` (2.0.0-canary.10+) renders one page with an empty chunk `[]`.

## Checked

2026-11-08. Confirmed against the Eleventy docs Pagination page (markdown source): `data` and `size`, the example output paths, the `pagination` object entries, the backwards-compatible older names, global/local data and collection sources, `alias` behaviour and the reserved `page` name, and `generatePageOnEmptyData`. Added the version note for `generatePageOnEmptyData`. Nothing removed. The page's front matter example is shown through an include, so the YAML above is a reconstruction of the described shape.

Method: documentation only; no commands were run.
