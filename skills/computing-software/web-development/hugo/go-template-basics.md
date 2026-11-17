---
id: computing-software.web-development.hugo.go-template-basics
name: go-template-basics
category: computing-software
field: web-development
product: hugo
tags: [go-templates, context, variables, whitespace, comments]
level: intro
status: docs-checked
description: "Go template basics in Hugo: the dot context and $, variables, whitespace trimming, pipes, index, comments that avoid HTML delimiters, and calling partials."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo templates use Go's `text/template` and `html/template` packages; HTML files use `html/template`.

- The dot `.` is the current context. Inside `range` or `with`, `$` accesses the template's original context.
- `{{-` and `-}}` remove adjacent whitespace.
- Double quotes: interpreted strings; backticks: raw strings.
- A piped value becomes the final argument of the next function or method.
- `:=` initializes a variable and `=` reassigns it. Variables in `if`, `range` or `with` are scoped to the block.
- Use `index` for slices, maps and keys that are not valid identifiers, such as hyphenated keys. Slices are zero-based.

```go-html-template
{{ $total := 3 }}
{{ range slice 7 11 21 }}
  {{ $total = add $total . }}
{{ end }}
{{ $total }} → 42
```

```go-html-template
{{ "Hugo" | strings.ToLower | strings.TrimSuffix "o" }} → hug
{{ index .Params "key-with-hyphens" }}
```

```go-html-template
{{ with "foo" }}
  <p>{{ $.Title }} - {{ . }}</p>
{{ end }}
```

Comments: do not use HTML comment delimiters to comment out template code, because Hugo still evaluates code inside them. Use:

```go-html-template
{{/* This is an inline comment. */}}
```

To emit an HTML comment: `{{ "<!-- I am an HTML comment. -->" | safeHTML }}`.

Partials live in `layouts/_partials`; pass the current context:

```go-html-template
{{ partial "breadcrumbs.html" . }}
{{ partialCached "css.html" . }}
```

## Checked

2026-11-04: html/template default, dot and $ context, whitespace trimming, quote types, pipes, variable scope, index, comment rules, safeHTML for HTML comments and partial directory confirmed against the Hugo docs Introduction to templating page. Nothing removed.

Method: documentation only; no commands were run.
