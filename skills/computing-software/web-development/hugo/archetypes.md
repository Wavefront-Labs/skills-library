---
id: computing-software.web-development.hugo.archetypes
name: archetypes
category: computing-software
field: web-development
product: hugo
tags: [archetypes, hugo-new-content, front-matter-template, leaf-bundle-archetype, kind-flag]
level: practitioner
status: docs-checked
description: "Write Hugo archetypes for hugo new content: lookup order, template context fields, date formatting, bundle archetypes and the --kind flag."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/archetypes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An archetype is a template for new content. `hugo new content` creates a file in `content` and evaluates template actions in the archetype at creation time.

Lookup order for `hugo new content posts/my-first-post.md` with theme `my-theme`:

1. `archetypes/posts.md`
2. `themes/my-theme/archetypes/posts.md`
3. `archetypes/default.md`
4. `themes/my-theme/archetypes/default.md`

If none exists, Hugo uses a built-in default.

Context: `Date` (RFC3339 string), `File`, `Type` (top-level directory or the `--kind` flag) and `Site`. Any template function works.

```md
+++
title = '{{ replace .File.ContentBaseName `-` ` ` | title }}'
date = '{{ time.Now.Format "2006-01-02" }}'
draft = true
+++
```

Actions in the body are also evaluated at creation only; put actions that must run on each build in a template.

Leaf bundle archetypes are directories (`archetypes/galleries/index.md` plus `archetypes/galleries/images/.gitkeep`). Subdirectories must contain at least one file or Hugo will not create them.

```sh
hugo new galleries/bryce-canyon
```

Pick an archetype explicitly:

```sh
hugo new content --kind tutorials articles/something.md
```

## Checked

2026-11-04: lookup order, context fields, date format example, leaf bundle archetype layout and --kind example confirmed against the Hugo docs Archetypes page. Nothing removed.

Method: documentation only; no commands were run.
