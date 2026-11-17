---
id: computing-software.web-development.hugo.render-segments
name: render-segments
category: computing-software
field: web-development
product: hugo
tags: [segments, render-segments, includes-excludes, partial-build, glob-filters]
level: advanced
status: docs-checked
description: "Render only part of a Hugo site with segments: includes and excludes filters on kind, output, path and sites, and the renderSegments setting or flag."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/segments.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Segmented rendering controls when content is rendered; it does not restrict access to Hugo's object graph. Benefits: faster builds, rapid development, scheduled rebuilds at different frequencies, and targeted output such as JSON search indexes.

Each segment has `includes` and `excludes` arrays of filters. A filter has one or more conditions comparing a page field to a glob pattern. Conditions in one filter are ANDed; filters in an array are ORed. `excludes` takes absolute precedence. Excluding output formats or sites is faster than including, because Hugo skips whole groups of pages.

Fields: `kind`, `output`, `path`, `sites` (new in 0.153.0, a sites matrix) and `lang` (deprecated in 0.153.0, use `sites`).

Exclude JSON output:

```toml
[segments.segment1]
  [[segments.segment1.excludes]]
    output = '! json'
```

Include only books and home, term and taxonomy kinds:

```toml
[[segments.segment1.includes]]
  kind = '{home,term,taxonomy}'
[[segments.segment1.includes]]
  path = '{/books,/books/**}'
```

Select segments with the setting or the flag; separate several with commas:

```sh
hugo build --renderSegments segment1,segment2
```

```toml
renderSegments = ['segment1','segment2']
```

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure segments: the scope note, the four benefits, the filter evaluation rules (AND within a filter, OR across filters, `excludes` precedence), the exclude-versus-include performance note, the fields with the 0.153.0 notes, the example filters and the `renderSegments` setting and flag. Nothing removed.

Method: documentation only; no commands were run.
