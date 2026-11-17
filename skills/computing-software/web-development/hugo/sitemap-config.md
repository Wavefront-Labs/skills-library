---
id: computing-software.web-development.hugo.sitemap-config
name: sitemap-config
category: computing-software
field: web-development
product: hugo
tags: [sitemap, changefreq, priority, sitemap-xml, front-matter]
level: intro
status: docs-checked
description: "Configure the Hugo sitemap: changefreq, priority, filename and disable, with defaults applied to all pages and overridable per page in front matter."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/sitemap.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/front-matter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The sitemap configuration sets defaults for all pages; front matter can override them per page via the `sitemap` field.

Settings:

- `changefreq` (string): `always`, `hourly`, `daily`, `weekly`, `monthly`, `yearly` or `never`. Default `""`, which omits the field.
- `disable` (bool): default `false`. Set to `true` in front matter to exclude a page.
- `filename` (string): default `sitemap.xml`.
- `priority` (float): 0.0 to 1.0. Default `-1`, which omits the field.

The values follow the sitemaps.org protocol definitions for `changefreq` and `priority`.

The front matter reference lists `sitemap` as a map of sitemap options, read with the `Sitemap` method. Set `disable` to `true` there to exclude a page.

## Checked

2026-11-04. Confirmed against the Hugo docs pages Configure sitemap and Front matter: the four settings with valid values and defaults, the omit-field behaviour for `""` and `-1`, the per-page front matter override and the `Sitemap` method. Nothing removed.

Method: documentation only; no commands were run.
