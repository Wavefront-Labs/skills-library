---
id: computing-software.web-development.hugo.permalinks-config
name: permalinks-config
category: computing-software
field: web-development
product: hugo
tags: [permalinks, url-patterns, page-kinds, target-matcher, fallback-pattern]
level: practitioner
status: docs-checked
description: "Set custom URL patterns with permalinks in map form by section and page kind, per language, or in array form with target page matchers and a fallback pattern."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/permalinks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`permalinks` defines custom URL patterns. The `url` front matter field overrides any matching pattern.

**Map form** is keyed by page kind (`home`, `page`, `section`, `taxonomy`, `term`) and top-level section. It does not support `target`.

```toml
[permalinks.page]
articles = '/blog/:year/:month/:slug/'
[permalinks.section]
articles = '/blog/'
```

For a multilingual site, nest it under the language, for example `[languages.de.permalinks.page]`.

**Array form** (new in v0.161.0) takes a required `pattern` and an optional `target` page matcher. Hugo applies the first matching entry.

```toml
[[permalinks]]
pattern = '/blog/'
[permalinks.target]
path = '/articles'
[[permalinks]]
pattern = '/blog/:year/:month/:slug/'
[permalinks.target]
path = '/articles/**'
```

Target by language with `[permalinks.target.sites.matrix]` and `languages = 'de'`.

Put an entry without `target` last to catch pages no earlier entry matched:

```toml
[[permalinks]]
pattern = '/:section/:slug/'
```

If `target` is omitted, the pattern applies to all pages.

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure permalinks: the `url` override, the map form and its page kinds, no `target` support in the map form, the per-language nesting, the array form (new in 0.161.0) with `pattern` and `target`, first-match behaviour, the language matrix example and the no-target fallback entry. Nothing removed.

Method: documentation only; no commands were run.
