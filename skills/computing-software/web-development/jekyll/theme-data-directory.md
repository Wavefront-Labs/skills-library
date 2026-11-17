---
id: computing-software.web-development.jekyll.theme-data-directory
name: theme-data-directory
category: computing-software
field: web-development
product: jekyll
tags: [theme-data, i18n-data, data-override, theme-config-vs-data]
level: advanced
status: docs-checked
description: "Use the _data directory of a theme (4.3.0+) for overridable text such as translated headings, with the three file layouts a consumer can use and the config-vs-data rule."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From 4.3.0 Jekyll also reads a theme's `_data` directory, so data can be distributed with themes. Typical use: text inside design elements.

Instead of hard-coding a heading in an include such as `testimonials.html`, the theme refers to a text catalog, e.g. `site.data.i18n.testimonials.header`, and ships `_data/i18n/testimonials.yml` with the key `header`. A consumer overrides the text by supplying data, with no need to copy the include and lose theme updates.

The consumer's override of `site.data.i18n.testimonials.header` can sit in any of three places:

- `_data/i18n.yml` with key `testimonials.header`
- `_data/i18n/testimonials.yml` with key `header` (mirrors the theme's layout)
- `_data/i18n/testimonials/header.yml` with no key; the headline goes straight in the file

Theme authors should keep this ambiguity in mind when supporting consumers, since a mismatch can cause unforeseen trouble.

Rule of thumb: if a key changes the behaviour of the theme depending on whether it is present, it belongs in `site.config`; if it is data that is displayed anyway, `site.data` is fine. Bundling data that modifies theme behaviour is an anti-pattern, strongly discouraged. Theme authors must make every provided data item easy to override.

## Checked

2026-11-04. Confirmed against the Jekyll Themes page, themes with _data directory (4.3.0): the three override locations, the config-versus-data guidance and the anti-pattern note. Nothing removed.

Method: documentation only; no commands were run.
