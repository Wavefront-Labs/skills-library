---
id: computing-software.web-development.hugo.related-content-config
name: related-content-config
category: computing-software
field: web-development
product: hugo
tags: [related-content, indices, threshold, tokenize, pages-related]
level: practitioner
status: docs-checked
description: "Configure related content: threshold, includeNewer, weighted indices, tokenize and minTokenLength, and render related pages with Pages.Related in a partial."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/related-content.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo has default related-content configuration. Adding a `related` section requires a full configuration; you cannot override individual defaults alone.

Top-level settings:

- `threshold` (0-100): lower values return more, possibly less relevant, matches.
- `includeNewer` (default `false`): include newer pages in older posts' listings.
- `toLower` (default `false`): lowercase keywords in indexes and queries.

Per-index settings include `name`, `weight` (`0` turns the index off), `type` (`basic` or `fragments`), `pattern` (dates only), `cardinalityThreshold`, `applyFilter` and, from 0.166.0, `tokenize` and `minTokenLength`.

Weight authors twice as much as genres:

```toml
[related]
includeNewer = true
threshold = 80
toLower = true
[[related.indices]]
name = 'authors'
weight = 2
[[related.indices]]
name = 'genres'
weight = 1
```

Match shared title words:

```toml
[related]
threshold = 50
toLower = true
[[related.indices]]
name = 'title'
weight = 1
tokenize = true
minTokenLength = 4
```

Render in a partial:

```go-html-template
{{ with site.RegularPages.Related . | first 5 }}
  <ul>
    {{ range . }}
      <li><a href="{{ .RelPermalink }}">{{ .LinkTitle }}</a></li>
    {{ end }}
  </ul>
{{ end }}
```

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure related content: the full-configuration requirement, top-level and per-index settings with defaults and ranges, the 0.166.0 `tokenize` and `minTokenLength` notes, `weight` of 0, and both configuration examples and the partial. Nothing removed.

Method: documentation only; no commands were run.
