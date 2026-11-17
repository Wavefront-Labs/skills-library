---
id: computing-software.web-development.jekyll.front-matter-defaults
name: front-matter-defaults
category: computing-software
field: web-development
product: jekyll
tags: [front-matter-defaults, defaults-scope, scope-path-type, glob-defaults, precedence]
level: practitioner
status: docs-checked
description: "Set site-wide front matter with the defaults key: scope path and type, collections, glob patterns, precedence rules and the restart-on-config-change caveat."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/front-matter-defaults.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Put repeated front matter in `_config.yml` under `defaults`, an array of scope/values pairs:

```yaml
defaults:
  -
    scope:
      path: ""
      type: "posts"
    values:
      layout: "default"
```

- `path` is required; an empty string means all files. `type` is optional: `pages`, `posts`, `drafts` or a collection name (plural).
- Globs are limited to patterns containing `*` (3.7.0+), e.g. `path: "section/*/special-page.html"`. Globbing hurts build time in proportion to the collection directory size, especially on Windows.
- Precedence: a more specific `path` overrides a broader pair, e.g. `path: ""` pages get layout `my-site`, `path: "projects"` pages get `project` plus `author: "Mr. Hyde"`.
- Front matter in the file overrides defaults: a `projects/foo_project.md` with `author: "John Smith"` and `layout: "foobar"` wins over the scoped values.

Collection example:

```yaml
collections:
  my_collection:
    output: true
defaults:
  -
    scope:
      path: ""
      type: "my_collection"
    values:
      layout: "default"
```

`_config.yml` is read once at startup: stop and rerun `jekyll serve` after editing it. Data files do reload during regeneration.

## Checked

2026-11-04. Confirmed against the Jekyll front matter defaults doc: `defaults` array of scope/values pairs, required `path` and optional `type`, the available types, `*` globs with the 3.7.0 badge and performance warning, precedence examples (`my-site`, `project`, `Mr. Hyde`, `foobar`, `John Smith`), the collection example, and the restart note with data files. Nothing removed.

Method: documentation only; no commands were run.
