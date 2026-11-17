---
id: computing-software.web-development.hugo.render-hook-links
name: render-hook-links
category: computing-software
field: web-development
product: hugo
tags: [render-hook-link, render-link, external-links, embedded-link-hook, link-destination]
level: practitioner
status: docs-checked
description: "Write render-link.html: context fields, mark absolute links rel external, and how the embedded link hook resolves pages and resources."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/render-hooks/links.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A link render hook is `layouts/_markup/render-link.html`. A Markdown link has text, destination and optional title.

Context fields: `Destination`, `Ordinal` (new in v0.160.0), `Page`, `PageInner` (a page nested via `RenderShortcodes`), `PlainText`, `Position` (new in 0.160.0), `Text` (`template.HTML`) and `Title`.

CommonMark-equivalent output (use `{{- -}}` to trim whitespace around inline elements):

```go-html-template
<a href="{{ .Destination | safeURL }}"
  {{- with .Title }} title="{{ . }}"{{ end -}}
>
  {{- with .Text }}{{ . }}{{ end -}}
</a>
{{- /* chomp trailing newline */ -}}
```

Add `rel="external"` to absolute links:

```go-html-template
{{- $u := urls.Parse .Destination -}}
<a href="{{ .Destination | safeURL }}"
  {{- with .Title }} title="{{ . }}"{{ end -}}
  {{- if $u.IsAbs }} rel="external"{{ end -}}
>
  {{- with .Text }}{{ . }}{{ end -}}
</a>
{{- /* chomp trailing newline */ -}}
```

Embedded hook: resolves internal destinations by matching a page, then a page resource, then a global resource (which must be in `assets`). Remote destinations pass through, with no error or warning for unresolved ones.

```toml
[markup.goldmark.renderHooks.link]
useEmbedded = 'auto'
```

`auto` (default) uses it for multilingual single-host projects when duplication of shared page resources is disabled. Other values: `always`, `fallback`, `never`. Project, module and theme hooks take precedence. If resources are in `static`, mount `static` to `assets`.

## Checked

2026-11-04: hook path, context fields (Ordinal and Position new in 0.160.0), CommonMark-equivalent hook, rel=external example, embedded resolution order, useEmbedded values and default, and static-to-assets mount note confirmed against the Hugo docs Link render hooks page. Nothing removed.

Method: documentation only; no commands were run.
