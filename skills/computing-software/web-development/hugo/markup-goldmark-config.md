---
id: computing-software.web-development.hugo.markup-goldmark-config
name: markup-goldmark-config
category: computing-software
field: web-development
product: hugo
tags: [markup, goldmark, markdown-extensions, typographer, toc]
level: practitioner
status: docs-checked
description: "Configure Hugo's markup section: Goldmark extensions, subscript and strikethrough conflict, parser and renderer settings, footnotes, table of contents and other handlers."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/markup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo renders Markdown with Goldmark by default; `.md`, `.mdown` and `.markdown` files are Markdown unless front matter sets `markup`. `defaultMarkdownHandler` accepts `asciidocext`, `goldmark`, `org`, `pandoc` or `rst`. AsciiDoc, Pandoc and reStructuredText need an installed renderer and an updated security policy.

Goldmark extensions enabled by default: `cjk`, `definitionList`, `footnote`, `linkify`, `strikethrough`, `table`, `taskList`, `typographer`. `extras` and `passthrough` are off by default.

Subscript conflicts with Strikethrough, so disable strikethrough first:

```toml
[markup.goldmark.extensions]
strikethrough = false

[markup.goldmark.extensions.extras.subscript]
enable = true
```

Other Goldmark settings:

- `duplicateResourceFiles` (default `false`)
- `parser.autoHeadingID` and `parser.autoIDType` (default `github`; also `github-ascii`, `blackfriday`)
- `renderer.hardWraps` (default `false`)
- `renderer.unsafe` (default `false`)
- `renderHooks.image.useEmbedded` and `renderHooks.link.useEmbedded`: `auto` (default), `never`, `always` or `fallback`

Footnotes: `enable` defaults to `true`, `enableAutoIDPrefix` to `false`.

Table of contents defaults: `startLevel` 2, `endLevel` 3, `ordered` false.

Highlight settings apply to fenced code blocks, the `highlight` shortcode, `transform.Highlight` and `transform.HighlightCodeBlock`.

## Checked

2026-11-04. Confirmed against the Hugo docs page Configure markup: the default handler list and file extensions, the default-enabled Goldmark extensions, the subscript and strikethrough conflict example, the listed parser, renderer and render hook settings with defaults, the footnote defaults, the table of contents defaults and the highlight scope. Nothing removed.

Method: documentation only; no commands were run.
