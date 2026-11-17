---
id: computing-software.web-development.hugo.content-adapters
name: content-adapters
category: computing-software
field: web-development
product: hugo
tags: [content-adapters, content-gotmpl, addpage, addresource, dynamic-content]
level: advanced
status: docs-checked
description: "Create pages at build time from data with a _content.gotmpl content adapter: AddPage and AddResource maps, multilingual options and path collisions."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/content-adapters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A content adapter is a template named `_content.gotmpl` in `content`. It creates pages at build time from sources such as JSON, TOML, YAML or XML. Use no more than one per directory per language. Pages get logical paths relative to the adapter.

Methods: `AddPage`, `AddResource`, `Site` (not fully initialized, so `Site.Pages` errors), `Store`, `EnableAllLanguages` and `EnableAllDimensions`. By default the adapter runs once for the first matching site; `EnableAllLanguages` runs it for all languages.

```go-html-template
{{ $content := dict
  "mediaType" "text/markdown"
  "value" "The _Hunchback of Notre Dame_ was written by Victor Hugo."
}}
{{ $page := dict
  "content" $content
  "kind" "page"
  "path" "the-hunchback-of-notre-dame"
  "title" "The Hunchback of Notre Dame"
}}
{{ .AddPage $page }}
```

Page map: set front matter keys, except use `content.mediaType` instead of `markup` and put taxonomies like `tags` inside `params`. `path` is required, with no leading slash or extension. `content.mediaType` defaults to `text/markdown`.

Resource map: `content.mediaType`, `content.value` and `path` are required. A string `content.value` makes a resource published relative to the page; an existing resource is published relative to the site root, which is more efficient.

Multilingual: one adapter with `EnableAllLanguages`, per-language names like `_content.de.gotmpl`, or per-language content directories.

Pages sharing a publication path collide with indeterminate output; detect with `--printPathWarnings`.

## Checked

2026-11-04. Confirmed against the Hugo docs page Content adapters: the `_content.gotmpl` name and one-per-directory-per-language rule, the six methods, the not-fully-initialized `Site` note, the page and resource map keys and requirements, the string-versus-resource `content.value` behaviour, the multilingual options and the `--printPathWarnings` flag. Nothing removed.

Method: documentation only; no commands were run.
