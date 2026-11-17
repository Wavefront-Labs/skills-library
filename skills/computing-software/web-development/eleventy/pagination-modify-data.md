---
id: computing-software.web-development.eleventy.pagination-modify-data
name: pagination-modify-data
category: computing-software
field: web-development
product: eleventy
tags: [pagination-reverse, pagination-filter, pagination-before, order-of-operations]
level: practitioner
status: docs-checked
description: "Change Eleventy pagination data before paging with reverse, filter and the before callback, and know the order they run in."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/pagination.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three ways to alter the data set before it is chunked.

**reverse** (0.7.0+): `reverse: true` reverses the data. `testdata` of item1..item4 with `size: 2` pages as `[["item4","item3"],["item2","item1"]]`.

**filter** (0.4.0+): removes values from the paginated data.

```yaml
pagination:
  data: testdata
  size: 1
  filter:
    - item3
```

Works the same for paginated arrays, and for objects: the page's example filters an object by key, and with `resolve: values` the filter lists values (`itemvalue3`).

**before** (0.10.0+): a callback for any change (sort, filter, map, slice). The page's example uses JavaScript front matter (`---js`). `fullData` (1.0.1+) is the full data cascade so far.

```md
---js
{
  pagination: {
    data: "testdata",
    size: 2,
    before: function (paginationData, fullData) {
      return paginationData.map(entry => `${entry} with a suffix`);
    }
  },
  testdata: ["item1", "item2", "item3", "item4"]
}
---
```

JavaScript template functions (universal filters and shortcodes) are available as `this` in `before` from 2.0.0-canary.16, e.g. `this.slugify("My title.")`.

**Order of operations:** `before`, then `reverse`, then `filter`.

## Checked

2026-11-08. Confirmed against the Eleventy docs Pagination page (markdown source): reverse, filter, the `before` callback and its `fullData` argument, template functions in `before`, version notes and the order of operations. Reworded the "needs JavaScript front matter" and filter-on-objects lines to what the page's examples show. Nothing else removed.

Method: documentation only; no commands were run.
