---
id: computing-software.web-development.hugo.cascade-config
name: cascade-config
category: computing-software
field: web-development
product: hugo
tags: [cascade, page-matcher, target, params, front-matter]
level: practitioner
status: docs-checked
description: "Pass values down to pages with cascade in site configuration: map and array forms, and limiting them with a target page matcher by path and language."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/cascade.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/front-matter.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`cascade` passes values down to pages. It has a map form for a single cascade and an array form for different values on different subsets. Both support `target`, a page matcher; if omitted, values cascade to all pages.

Map form:

```toml
[cascade.params]
color = 'red'
```

Array form:

```toml
[[cascade]]
[cascade.params]
color = 'red'
[cascade.target]
path = '{/articles,/articles/**}'
[[cascade]]
[cascade.params]
color = 'blue'
[cascade.target]
path = '{/tutorials,/tutorials/**}'
```

Limit by language as well:

```toml
[cascade.target.sites.matrix]
languages = '{en,de}'
```

Cascade can also be set in a page's front matter, for example in `content/_index.md`:

```toml
title = 'Home'
[cascade.params]
color = 'red'
```

The older `_target` key is deprecated; use `target`. In multilingual projects, defining cascade values in project configuration is often more efficient.

In `config` directory files, slice-typed keys such as `cascade` need their category name.

## Checked

2026-11-04. Confirmed against the Hugo docs pages Configure cascade, Front matter and Configure Hugo: the map and array forms, `target` page matcher and the language matrix example, front matter cascade, the `_target` deprecation, the multilingual efficiency note and the category-name rule for slice-typed keys. Nothing removed.

Method: documentation only; no commands were run.
