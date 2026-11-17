---
id: computing-software.web-development.hugo.shortcode-templates
name: shortcode-templates
category: computing-software
field: web-development
product: hugo
tags: [shortcode-templates, inner, parent, isnamedparams, hasshortcode]
level: practitioner
status: docs-checked
description: "Write custom Hugo shortcode templates in layouts/_shortcodes: named and positional arguments, Inner content, Parent, nesting order and HasShortcode."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/templates/shortcode.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shortcode templates go in `layouts/_shortcodes`, at the root or in subdirectories. A subdirectory shortcode is called by its path without the extension (`media/audio`). Hugo selects by shortcode name, output format and language, most specific first.

```go-html-template
{{- now.Format "2006" -}}
```

Saved as `layouts/_shortcodes/year.html`, it is called as `{{< year >}}`.

Arguments are named or positional, not both in one call. `IsNamedParams` tells which; `Params` is a map (named) or slice (positional). Support both:

```go-html-template
{{ $path := cond (.IsNamedParams) (.Get "path") (.Get 0) }}
{{ $width := cond (.IsNamedParams) (.Get "width") (.Get 1) }}
```

`Inner` returns enclosed content. With standard notation, convert Markdown with `RenderString`; Markdown notation does not need it.

```go-html-template
<div class="contrived">
  <h2>{{ .Get "title" }}</h2>
  {{ .Inner | .Page.RenderString }}
</div>
```

`Parent` lets a nested shortcode inherit from its parent:

```go-html-template
{{ with .Parent }}
  <img src="{{ $src }}" class="{{ .Get "class" }}-image">
{{ else }}
  <img src="{{ $src }}">
{{ end }}
```

Rendering order: Markdown-notation shortcodes run before the Markdown renderer, standard notation after. Nested shortcodes render inside out.

`HasShortcode` checks use on a page, for example to load CSS conditionally:

```go-html-template
{{ if .HasShortcode "audio" }}...{{ end }}
```

## Checked

2026-11-04: directory and subdirectory call path, lookup by name/output format/language, year.html example, IsNamedParams and Params, Inner with RenderString, Parent, rendering order and HasShortcode confirmed against the Hugo docs Shortcode templates page. Nothing removed.

Method: documentation only; no commands were run.
