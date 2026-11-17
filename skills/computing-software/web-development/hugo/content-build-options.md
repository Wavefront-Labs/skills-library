---
id: computing-software.web-development.hugo.content-build-options
name: content-build-options
category: computing-software
field: web-development
product: hugo
tags: [build-options, headless, list-render, publish-resources, hide-section]
level: advanced
status: docs-checked
description: "Use the build front matter object (list, render, publishResources) to make headless pages, list without publishing, publish without listing, or hide a section in production."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build options live in a reserved `build` front matter object:

- `list`: `always` (default), `local` or `never`; inclusion in page collections.
- `render`: `always` (default), `link` or `never`; whether the page is written to disk.
- `publishResources`: `true` (default) or `false`; applies to page bundles.

`Page.GetPage` and `Site.GetPage` can always find any page.

**Headless page** (a leaf bundle, unpublished, reusable elsewhere):

```toml
title = 'Headless page'
[build]
  list = 'never'
  publishResources = false
  render = 'never'
```

```go-html-template
{{ with site.GetPage "/headless" }}
  {{ .Content }}
{{ end }}
```

Resources are still published if you call `RelPermalink` on them.

**Headless section:** cascade the options to descendants.

```toml
[[cascade]]
[cascade.build]
  list = 'local'
  publishResources = false
  render = 'never'
```

**Publish without listing** (descendants published, section page not):

```toml
[build]
render = 'never'
list = 'never'
```

**Hide a section only in production**, using cascade with a target:

```toml
[[cascade]]
[cascade.build]
render = 'never'
list = 'never'
[cascade.target]
environment = 'production'
```

## Checked

2026-11-04. Confirmed against the Hugo docs page Build options: the `build` defaults and values of `list`, `render` and `publishResources`, the `GetPage` note, the headless page, headless section, publish-without-listing and conditional-hide examples, and the RelPermalink resource-publishing behaviour. Nothing removed.

Method: documentation only; no commands were run.
