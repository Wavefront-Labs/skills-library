---
id: computing-software.web-development.jekyll.front-matter
name: front-matter
category: computing-software
field: web-development
product: jekyll
tags: [front-matter, yaml-header, layout-variable, published-flag, custom-variables]
level: intro
status: docs-checked
description: "Write Jekyll front matter: triple-dash YAML block, predefined layout, permalink, published, date, categories and tags variables, and custom variables."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/front-matter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A file with a YAML front matter block is processed by Jekyll. The block must be first in the file, between triple-dashed lines:

```yaml
---
layout: post
title: Blogging Like a Hacker
---
```

An empty block (two dashed lines) still makes Jekyll process the file; useful for CSS and RSS feeds. Variables are available via Liquid in the file, its layouts and includes. With UTF-8, make sure there is no BOM header, especially on Windows.

Predefined globals:

- `layout`: layout file name without extension, from `_layouts`. `null` produces a file with no layout (overridden by a layout in front matter defaults for posts/documents). From 3.5.0, `none` in a post/document skips the layout regardless of defaults; in a page it looks for a layout named "none".
- `permalink`: final URL, replacing the site-wide style.
- `published`: `false` hides the post at generation. Preview with `--unpublished`.

Post variables:

- `date`: overrides the file-name date; format `YYYY-MM-DD HH:MM:SS +/-TTTT` (time and offset optional).
- `category` / `categories`: YAML list or space-separated string.
- `tags`: same forms.

Custom variables are read as `page.<name>`:

```liquid
---
food: Pizza
---
<h1>{{ page.food }}</h1>
```

Repeated values belong in front matter defaults.

## Checked

2026-11-04. Confirmed against the Jekyll front matter doc: triple-dash YAML at the top of the file, empty block still processed, BOM warning, `layout` (`null`, and `none` from 3.5.0), `permalink`, `published` with `--unpublished`, post `date` format, `category`/`categories`, `tags`, custom `page.<name>` variables, and the defaults tip. Nothing removed.

Method: documentation only; no commands were run.
