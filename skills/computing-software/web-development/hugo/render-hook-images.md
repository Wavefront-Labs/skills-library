---
id: computing-software.web-development.hugo.render-hook-images
name: render-hook-images
category: computing-software
field: web-development
product: hugo
tags: [render-hook-image, render-image, figure, embedded-image-hook, standalone-images]
level: practitioner
status: docs-checked
description: "Write render-image.html: context fields, standalone images as figure elements, and the embedded image hook with its useEmbedded modes."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/render-hooks/images.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An image render hook is `layouts/_markup/render-image.html`. A Markdown image has description, destination and optional title.

Context: `Attributes`, `Destination`, `IsBlock`, `Ordinal` (zero-based, new in v0.160.0), `Page`, `PageInner`, `PlainText`, `Position` (new in 0.160.0), `Text` and `Title`.

- `Attributes` needs Markdown attributes enabled: `wrapStandAloneImageWithinParagraph = false` and `block = true`.
- `IsBlock` is true for a standalone image not wrapped in a paragraph.

```toml
[markup.goldmark.parser]
wrapStandAloneImageWithinParagraph = false
[markup.goldmark.parser.attribute]
block = true
```

CommonMark-equivalent hook (the `{{- -}}` delimiters trim whitespace around inline elements):

```go-html-template
<img src="{{ .Destination | safeURL }}"
  {{- with .PlainText }} alt="{{ . }}"{{ end -}}
  {{- with .Title }} title="{{ . }}"{{ end -}}
>
{{- /* chomp trailing newline */ -}}
```

Standalone images as figures (the docs version also has an `else` branch that renders inline images with `src`, `alt` and `title`):

```go-html-template
{{- if .IsBlock -}}
  <figure>
    <img src="{{ .Destination | safeURL }}" {{- with .PlainText }} alt="{{ . }}"{{ end -}}>
    {{- with .Title }}<figcaption>{{ . }}</figcaption>{{ end -}}
  </figure>
{{- end -}}
```

Embedded hook: resolves internal destinations to a page resource, then a global resource (in `assets`); passes remote ones through; no error or warning when unresolved; no image processing. `markup.goldmark.renderHooks.image.useEmbedded` is `auto` (default), `always`, `fallback` or `never`. Custom hooks take precedence. To resolve files in `static`, mount `static` to `assets` with two `module.mounts` entries.

## Checked

2026-11-04: context fields (Ordinal and Position new in 0.160.0), Attributes settings, CommonMark-equivalent and figure hooks, useEmbedded values and default, embedded resolution order, no-processing note and static-to-assets mounts confirmed against the Hugo docs Image render hooks page. Added a note that the figure example omits the page's else branch.

Method: documentation only; no commands were run.
