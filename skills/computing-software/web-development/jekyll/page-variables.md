---
id: computing-software.web-development.jekyll.page-variables
name: page-variables
category: computing-software
field: web-development
product: jekyll
tags: [page-variables, page-url, page-date, page-next-previous, page-excerpt, page-dir]
level: practitioner
status: docs-checked
description: "Use Jekyll page.* variables: url, date, id, categories, tags, collection, dir, name, path, slug, ext, next, previous, excerpt and content, with their caveats."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_variables.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `page.content`: rendered or unrendered depending on what Liquid is being processed.
- `page.title`.
- `page.excerpt`: unrendered excerpt; override in front matter. Disable per document by setting `excerpt_separator` to an empty string in its front matter, or site-wide as a top-level config key.
- `page.url`: no domain, leading slash, e.g. `/2008/12/14/my-post.html`.
- `page.date`: posts only. Override with `YYYY-MM-DD HH:MM:SS` (UTC assumed) or with an offset, e.g. `2008-12-14 10:30:00 +0900`.
- `page.id`: unique per post or collection document, e.g. `/2008/12/14/my-post`. Not for pages.
- `page.categories`: from directories above `_posts`, e.g. `['work', 'code']`, plus front matter. Path-based categories may not work for user-defined collections.
- `page.tags`.
- `page.collection`: collection label (`posts`), or an empty string if none.
- `page.dir`: path between the source and the page's file, e.g. `/pages/`. Derived from `url`, so `permalink` overrides it. Not applicable to posts or user-defined collection documents.
- `page.name`: filename, e.g. `about.md`.
- `page.path`: raw path relative to source; overridable in front matter.
- `page.slug`: filename without extension or date prefix; overridable.
- `page.ext`: file extension; overridable.
- `page.next` / `page.previous`: neighbours in `site.posts`; `nil` at the last / first entry.

## Checked

2026-11-04. Each entry compared with the page section of the Jekyll variables data file: content, title, excerpt (including the empty `excerpt_separator` rule), url, date formats, id, categories, collection, tags, dir, name, path, slug, ext, next and previous, with their caveats. Nothing removed.

Method: documentation only; no commands were run.
