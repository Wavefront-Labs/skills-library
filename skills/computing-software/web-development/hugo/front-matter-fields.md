---
id: computing-software.web-development.hugo.front-matter-fields
name: front-matter-fields
category: computing-software
field: web-development
product: hugo
tags: [front-matter, reserved-fields, params, dates, time-zone]
level: intro
status: docs-checked
description: "Hugo front matter: TOML, YAML and JSON formats, reserved fields such as title, date, draft, slug, type and layout, custom params, and date time zone precedence."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/front-matter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Front matter is metadata at the top of a content file. Hugo detects TOML, YAML or JSON from the delimiters. Field types: boolean, integer, float, string, arrays, maps (TOML also has unquoted date/time).

Reserved field names cannot be used for custom fields; put custom fields under `params` and read them with `Params` or `Param`.

```toml
title = 'Example'
date = 2024-02-02T04:14:54-08:00
draft = false
weight = 10
[params]
author = 'John Smith'
```

Selected fields:

- `aliases`, `build`, `cascade`, `outputs`, `sitemap`, `sites`, `resources`
- `date`, `publishDate` (alias `pubdate`, `published`), `expiryDate` (alias `unpublishdate`), `lastmod` (alias `modified`)
- `description`, `keywords`, `summary`, `title`, `linkTitle`
- `draft`, `headless` (leaf bundles: sets `render` and `list` to `never`)
- `layout` (template base name), `type` (content type), `markup`
- `slug`, `url`, `translationKey`, `weight`
- `menus` (alias `menu`), `isCJKLanguage`

Taxonomy terms use the plural taxonomy name as the key.

Date fields must use a parsable format. Time zone precedence: the offset in the date string, then `timeZone` in project configuration, then `Etc/UTC`.

For Org Mode content front matter uses keywords such as `#+TITLE:` and `#+TAGS[]: red blue`.

## Checked

2026-11-04: formats and field types, reserved-field rule, params, listed fields and aliases, headless, taxonomy keys, time zone precedence and Org Mode keywords confirmed against the Hugo docs Front matter page. Nothing removed.

Method: documentation only; no commands were run.
