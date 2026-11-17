---
id: computing-software.web-development.hugo.partial-caching
name: partial-caching
category: computing-software
field: web-development
product: hugo
tags: [partialcached, partials-includecached, variant-cache-key, performance]
level: practitioner
status: docs-checked
description: "Cache partial output with partialCached: LAYOUT, CONTEXT and VARIANT arguments, per-site caches, parallel rendering caveat and return values."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/functions/partials/IncludeCached.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/troubleshooting/performance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`partials.IncludeCached` (alias `partialCached`) returns the cached result of rendering a partial, optionally keyed by variants. The first call renders and caches; later calls with the same `LAYOUT` and variant values return the cache, even if `CONTEXT` differs.

Arguments:

- `LAYOUT`: partial path relative to `layouts/_partials`. A leading `./` or `../` resolves relative to the calling partial.
- `CONTEXT`: the data passed in. Unlike `partials.Include`, it is required; pass `nil` for none.
- `VARIANT` (optional): one or more values of any type forming a unique cache key. The partial cannot access them.

Notes:

- Each site (for example each language) has its own cache, so each renders the partial at least once.
- Pages render in parallel, so concurrent calls may render the partial more than once before the result is cached.
- If the partial has a `return` statement, that value is returned; otherwise the output as `template.HTML` or `string`.

Good fits: sidebars and menus that run many times per build, one result per section, or per combination such as country and province.

Find candidates with `hugo build --templateMetrics --templateMetricsHints`; a partial at 100% cache potential is a candidate, but review side effects first.

## Checked

2026-11-04. Confirmed against the Hugo docs pages partials.IncludeCached and Performance: the alias and signature, first-call caching and variant keys, per-site caches, the parallel rendering caveat, return values, the `./` and `../` rule, the `nil` context, the section and country examples, `--templateMetrics --templateMetricsHints`, and the 100% cache potential side-effect warning. Nothing removed.

Method: documentation only; no commands were run.
