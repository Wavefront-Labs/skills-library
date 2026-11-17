---
id: computing-software.web-development.jekyll.incremental-regeneration
name: incremental-regeneration
category: computing-software
field: web-development
product: jekyll
tags: [incremental-build, jekyll-metadata, regenerate-true, build-performance]
level: practitioner
status: docs-checked
description: "Speed up rebuilds with experimental incremental regeneration: what it tracks, its blind spots, the regenerate front matter override and how to enable it."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/incremental-regeneration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Incremental regeneration builds only documents and pages updated since the previous build. It records file modification times and inter-document dependencies in `.jekyll-metadata`. It is experimental and does not work in every scenario, so use it cautiously.

A document or page is regenerated only if it or one of its tracked dependencies changed. The only dependencies tracked are includes (via the include tag) and layouts. A plain reference to other documents, such as looping over `site.posts` on a listing page, is not detected.

Workaround: put `regenerate: true` in a document's front matter to force it to regenerate every build. This regenerates only that document; references to other documents' content will not work because those are not re-rendered.

Enable it with the flag or the config key:

```sh
jekyll serve --incremental
```

```yaml
incremental: true
```

`-I` is the short flag.

## Checked

2026-11-04. Confirmed against the Jekyll incremental regeneration doc: experimental warning, `.jekyll-metadata` tracking, tracked dependency types (includes and layouts), the `site.posts` blind spot, `regenerate: true` and its limit, `--incremental` / `-I` and `incremental: true`. Removed the advice to add `.jekyll-metadata` to `.gitignore`, which the page does not state.

Method: documentation only; no commands were run.
