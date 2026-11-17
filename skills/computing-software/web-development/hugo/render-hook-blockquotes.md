---
id: computing-software.web-development.hugo.render-hook-blockquotes
name: render-hook-blockquotes
category: computing-software
field: web-development
product: hugo
tags: [render-hook-blockquote, alerts, callouts, blockquote-attributes, render-blockquote]
level: practitioner
status: docs-checked
description: "Write render-blockquote.html: context fields, regular versus alert blockquotes, basic and extended alert syntax, and citation attributes."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/render-hooks/blockquotes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A blockquote hook is `layouts/_markup/render-blockquote.html`, or split into `render-blockquote-alert.html` and `render-blockquote-regular.html`. By default Hugo follows CommonMark.

Context:

- `Type`: `alert` or `regular`.
- Alerts only: `AlertType` (lowercase), `AlertTitle` (`template.HTML`), `AlertSign` (`+`, `-` or empty).
- `Attributes` (needs `markup.goldmark.parser.attribute` with `block = true`), `Ordinal`, `Page`, `PageInner`, `Position`.
- `Text` (`template.HTML`); for alerts it excludes the first line.

Alert syntax (compatible with GitHub, Obsidian and Typora):

```md
> [!NOTE]
> Useful information that users should know, even when skimming content.
```

Types shown: NOTE, TIP, IMPORTANT, WARNING, CAUTION. Extended syntax (alert sign and/or title) works in Obsidian only; GitHub and Typora render it as a regular blockquote:

```md
> [!WARNING]+ Radiation hazard
> Do not approach or handle without protective gear.
```

Citation and caption via attributes:

```md
> Some text
{cite="https://gohugo.io" caption="Some caption"}
```

```go-html-template
<figure>
  <blockquote {{ with .Attributes.cite }}cite="{{ . }}"{{ end }}>
    {{ .Text }}
  </blockquote>
  {{ with .Attributes.caption }}<figcaption>{{ . | safeHTML }}</figcaption>{{ end }}
</figure>
```

An alert title can fall back to `{{ or (i18n .AlertType) (title .AlertType) }}`.

## Checked

2026-11-04: hook file names, context fields and types, attribute setting, alert types and syntax, Obsidian-only extended syntax, figure/citation example and title fallback confirmed against the Hugo docs Blockquote render hooks page. Nothing removed.

Method: documentation only; no commands were run.
