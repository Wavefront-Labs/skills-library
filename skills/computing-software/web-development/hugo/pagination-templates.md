---
id: computing-software.web-development.hugo.pagination-templates
name: pagination-templates
category: computing-software
field: web-development
product: hugo
tags: [pagination, paginate, paginator, pager, pagination-partial]
level: practitioner
status: docs-checked
description: "Paginate Hugo list pages with Paginate or Paginator, group before paginating, use the embedded pagination partial, and configure pagerSize, path and disableAliases."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/pagination.md
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/pagination.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pagination splits a list page (`home`, `section`, `taxonomy`, `term`) into pagers. Configure it with `pagerSize` (default 10), `path` (default `page`) and `disableAliases` (default `false`; `true` removes the alias for the first pager). Languages can set their own under `[languages.<key>.pagination]`.

`Paginate` works on any page collection and can override `pagerSize`:

```go-html-template
{{ $pages := where site.RegularPages "Type" "posts" }}
{{ $paginator := .Paginate $pages.ByTitle 7 }}

{{ range $paginator.Pages }}
  <h2><a href="{{ .RelPermalink }}">{{ .LinkTitle }}</a></h2>
{{ end }}

{{ partial "pagination.html" . }}
```

`Paginator` paginates only the collection passed into the template and cannot override `pagerSize`:

```go-html-template
{{ range .Paginator.Pages }}...{{ end }}
```

Group first with `$paginator.PageGroups`:

```go-html-template
{{ $paginator := .Paginate ($pages.GroupByDate "Jan 2006") }}
```

Cautions:

- The first invocation is cached; later ones reuse it and do not behave as written. Invoke pagination once per list page.
- Do not use `compare.Conditional` for conditional pagination, since it evaluates both arguments eagerly. Use `if-else`.

The embedded `pagination.html` partial has `default` and `terse` formats. Pass a format with `dict "page" . "format" "terse"`. Copy its source to `layouts/_partials` under the same name to override.

## Checked

2026-11-04: pagerSize, path and disableAliases defaults, per-language pagination, Paginate versus Paginator, grouping example, caching caution, compare.Conditional warning and the default/terse partial formats confirmed against the Hugo docs Pagination template page and the Configure pagination page. Nothing removed.

Method: documentation only; no commands were run.
