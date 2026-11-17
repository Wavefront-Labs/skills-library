---
id: computing-software.web-development.eleventy.collection-items-and-sorting
name: collection-items-and-sorting
category: computing-software
field: web-development
product: eleventy
tags: [collection-items, collection-sort-order, array-reverse-pitfall, content-date]
level: practitioner
status: docs-checked
description: "Read the data shape of Eleventy collection items, understand the default date sort, and reverse collections without mutating them."
sources:
  - https://www.11ty.dev/docs/collections/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each collection item has:

- `page`: Eleventy's supplied page variable for that template (`inputPath`, `url`, `date`, ...)
- `data`: all data for the content, including data inherited from layouts (`post.data.title`)
- `rawInput`: raw template input before processing, without front matter (3.0.0+)
- `content`: rendered content, without layout wrappers (alias of older `templateContent`)

Older top-level `inputPath`, `fileSlug`, `outputPath`, `url`, `date` still exist; prefer `page.*`.

**Default sort**, ascending: the input file's created date (override with `date` in front matter), ties broken by full input path including filename.

**Never call Array `reverse()` on a collection in a template or shortcode.** It reorders the array in place and affects every other use of that collection. Instead use:

- JavaScript `.toReversed()` (Node 20+)
- `.filter(entry => entry).reverse()` on a fresh copy
- Liquid's or Nunjucks' `reverse` filter

```njk
{% for post in collections.post | reverse %}
```

Override a page's sort position by setting its `date` in front matter (`date: 2016-01-01`); see the dates skill.

## Checked

2026-11-04. Confirmed against the Eleventy Collections page: item fields page, data, rawInput (v3.0.0) and content (v2.0.0, alias of templateContent), backward-compatible top-level properties, the default ascending sort by created date with full-path tie-break, the Array reverse() pitfall and its alternatives (toReversed on Node 20+, filter then reverse, Liquid and Nunjucks reverse), and the date override. Corrected the rawInput version gate from 3.0.0-alpha.1 to 3.0.0.

Method: documentation only; no commands were run.
