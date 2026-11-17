---
id: computing-software.web-development.hugo.outputs-per-page-kind
name: outputs-per-page-kind
category: computing-software
field: web-development
product: hugo
tags: [outputs, page-kinds, primary-output-format, json-output, front-matter-outputs]
level: practitioner
status: docs-checked
description: "Choose which output formats Hugo renders for each page kind, why the first format is primary, and add formats to a single page with the outputs front matter field."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/outputs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `outputs` configuration sets the output formats generated for each page kind. To render the built-in `json` format for the home page, you need a template for it, then add an entry:

```toml
[outputs]
home = ['html','rss','json']
```

- Only list page kinds whose defaults you want to change.
- Order matters. The first format is the primary output format for that page kind, usually `html`.
- The primary format determines what `Permalink` and `RelPermalink` return on a `Page`. For formats with `permalinkable` set to `true`, such as `html` and `amp`, those methods return that format's own URL regardless of position.

Per-page outputs use front matter. They append to the configured outputs rather than replacing them:

```toml
title = 'Example'
outputs = ['json']
```

By default, a page with `outputs = ['json']` renders both `html` and `json`.

## Checked

2026-11-04: outputs per page kind example, primary-format rule, permalinkable note and per-page outputs behaviour confirmed against the Hugo docs Configure outputs page. Removed a cross-reference sentence the page does not contain.

Method: documentation only; no commands were run.
