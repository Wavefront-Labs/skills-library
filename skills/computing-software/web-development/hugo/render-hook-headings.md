---
id: computing-software.web-development.hugo.render-hook-headings
name: render-hook-headings
category: computing-software
field: web-development
product: hugo
tags: [render-hook-heading, render-heading, heading-anchors, heading-attributes]
level: practitioner
status: docs-checked
description: "Write render-heading.html: context fields, enabling heading attributes, and adding an anchor link to the right of each heading."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/render-hooks/headings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A heading render hook is `layouts/_markup/render-heading.html`. By default Hugo renders headings per the CommonMark specification, plus automatic `id` attributes.

Context fields:

- `Anchor` (string): the heading's `id`.
- `Attributes` (map): Markdown attributes; available when `title = true` is set under `[markup.goldmark.parser.attribute]`.
- `Level` (int): 1 through 6.
- `Ordinal` (int): zero-based position on the page, new in v0.160.0.
- `Page`, `PageInner` (a page nested via `RenderShortcodes`).
- `PlainText` (string) and `Text` (`template.HTML`).
- `Position` (string): new in 0.160.0.

```toml
[markup.goldmark.parser.attribute]
title = true
```

Default-equivalent hook:

```go-html-template
<h{{ .Level }} id="{{ .Anchor }}" {{- with .Attributes.class }} class="{{ . }}" {{- end }}>
  {{- .Text -}}
</h{{ .Level }}>
```

With an anchor link to the right of each heading:

```go-html-template
<h{{ .Level }} id="{{ .Anchor }}" {{- with .Attributes.class }} class="{{ . }}" {{- end }}>
  {{ .Text }}
  <a href="#{{ .Anchor }}">#</a>
</h{{ .Level }}>
```

## Checked

2026-11-04: hook path, CommonMark-plus-id default, context fields (Ordinal and Position new in 0.160.0), title attribute setting and both example hooks confirmed against the Hugo docs Heading render hooks page. Nothing removed.

Method: documentation only; no commands were run.
