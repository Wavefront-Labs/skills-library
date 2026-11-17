---
id: computing-software.web-development.jekyll.pagination-setup
name: pagination-setup
category: computing-software
field: web-development
product: jekyll
tags: [jekyll-paginate, paginate-config, paginate-path, paginator-object, pagination-limits]
level: practitioner
status: docs-checked
description: "Enable post pagination with jekyll-paginate: paginate and paginate_path config, output files, paginator attributes, and the limits (HTML index file, no permalink, posts only)."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/pagination.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_variables.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For Jekyll 3 or higher, add the `jekyll-paginate` gem to the Gemfile and to `plugins` in `_config.yml`.

```yaml
paginate: 5
paginate_path: "/blog/page:num/"
```

`paginate` is the maximum posts per page. With `paginate_path` above, Jekyll reads `blog/index.html`, passes each page in as `paginator`, and writes `blog/page:num/`, where `:num` starts at `2`. With 12 posts and `paginate: 5` you get `blog/index.html` (5 posts), `blog/page2/index.html` (5) and `blog/page3/index.html` (2).

Limits:

- Pagination works only from an HTML file named `index.html` (optionally in a subdirectory). It does not work from Markdown.
- Do not set `permalink` in that page's front matter; it breaks pagination.
- It pages through every post (except those with `hidden: true`). It cannot page by tag or category, and it cannot include collections.

`paginator` attributes: `page`, `per_page`, `posts`, `total_posts`, `total_pages`, `previous_page`, `previous_page_path`, `next_page`, `next_page_path`. The `previous_*`/`next_*` ones are `nil` when absent.

For categories, tags and collections use the third-party jekyll-paginate-v2, which GitHub Pages does not support.

## Checked

2026-11-04. Confirmed against the Jekyll pagination doc and the variables data file: plugin and Gemfile requirement, `paginate` and `paginate_path`, the 12-post example, HTML-only `index.html` limit, the no-permalink warning, the `hidden: true` and no tags/categories/collections limits, jekyll-paginate-v2 and GitHub Pages note, and all nine `paginator` attributes with their `nil` behaviour. Nothing removed.

Method: documentation only; no commands were run.
