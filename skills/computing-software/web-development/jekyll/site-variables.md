---
id: computing-software.web-development.jekyll.site-variables
name: site-variables
category: computing-software
field: web-development
product: jekyll
tags: [site-variables, global-variables, site-posts, site-pages, site-url, config-variables]
level: practitioner
status: docs-checked
description: "Know the Jekyll global variables (site, page, layout, jekyll, theme, content, paginator) and the site.* collections, time, url and custom config values."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/jekyll_variables.yml
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Globals: `site` (config plus site info), `page` (page info plus front matter), `layout` (layout front matter), `jekyll`, `theme`, `content` (only in layouts: the rendered page being wrapped), `paginator` (when `paginate` is set).

Custom front matter appears under `page`; layout front matter under `layout`, available in that layout and its parents.

`site.*`:

- `time`: when `jekyll` was run.
- `pages`, `posts` (reverse chronological), `static_files`, `html_pages`, `html_files`, `documents`, `collections` (including posts), `data`.
- `related_posts`: up to ten for a post; by default the most recent ten, or use `--lsi` for slow, higher-quality results (not supported on GitHub Pages).
- `categories.CATEGORY` and `tags.TAG`: posts in that category or with that tag.
- `url`: from the config. Under `jekyll serve` in development it becomes the host, port and SSL-derived URL, default `http://localhost:4000`.
- Any config key, e.g. `foo: bar` is `site.foo`. Changes to `_config.yml` are not picked up in watch mode; restart Jekyll.

`jekyll.version` and `jekyll.environment` (value of `JEKYLL_ENV`).

Theme variables (4.3.0+): `theme.root` (development only), `authors`, `description`, `version`, `dependencies`, `metadata`.

## Checked

2026-11-04. Confirmed against the Jekyll variables page and its variables data file: the global variable list, every `site.*` entry (including the `--lsi` and GitHub Pages note, `site.url` development behaviour and the watch-mode restart note), `jekyll.version`/`jekyll.environment`, the 4.3.0 badge on theme variables, and the layout front matter ProTip. Nothing removed.

Method: documentation only; no commands were run.
