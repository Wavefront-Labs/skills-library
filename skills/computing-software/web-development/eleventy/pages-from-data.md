---
id: computing-software.web-development.eleventy.pages-from-data
name: pages-from-data
category: computing-software
field: web-development
product: eleventy
tags: [pages-from-data, pagination-size-one, alias, data-driven-pages]
level: intro
status: docs-checked
description: "Generate one Eleventy page per data entry using pagination with size 1, an alias and a slugified permalink, for example from a global JSON data file."
sources:
  - https://raw.githubusercontent.com/11ty/11ty-website/main/src/docs/pages-from-data.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pagination is the way to make many output files from one data set, not only numbered pages. With `size: 1`, an alias and a `permalink` you get one page per entry.

Global data file `_data/possums.json` holds an array of objects with `name` and `age`. The template file name is unimportant, but its extension matters (`possum-pages.njk` or `.liquid`):

```md
---
pagination:
  data: possums
  size: 1
  alias: possum
permalink: "possums/{{ possum.name | slugify }}/"
---

{{ possum.name }} is {{ possum.age }} years old
```

Four entries produce four files, e.g. `/possums/fluffy/`. As entries are added or edited, the resulting pages update automatically.

`page` is a reserved word, so `alias: page` is not allowed (see Eleventy supplied data).

The page links to the Pagination docs sections on paging an object and remapping with permalinks.

## Checked

2026-11-08. Confirmed against the Eleventy docs Create Pages From Data page (markdown source): the possums example, file-name versus extension note, four generated files, the reserved page alias and the related links. Reworded the "next build" and "pagination skills" lines to what the page says. Note the page's sample data file shows JavaScript-style unquoted keys under a .json name; the skill only says an array of objects.

Method: documentation only; no commands were run.
