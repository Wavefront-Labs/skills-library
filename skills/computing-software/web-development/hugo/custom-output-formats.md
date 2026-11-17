---
id: computing-software.web-development.hugo.custom-output-formats
name: custom-output-formats
category: computing-software
field: web-development
product: hugo
tags: [output-formats, media-types, atom-feed, permalinkable, alternative-formats]
level: advanced
status: docs-checked
description: "Define and modify Hugo output formats: baseName, mediaType, isPlainText, permalinkable, weight, an Atom feed example, linking alternates and template names."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/configuration/output-formats.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A page may have several output formats, each resolving to a unique path. Properties: `baseName` (default `index`), `isHTML`, `isPlainText` (templates parsed with `text/template`), `mediaType`, `notAlternative`, `noUgly`, `path`, `permalinkable`, `protocol`, `rel`, `root`, `ugly` and `weight`.

Define only what differs from defaults. Render `json` before `html`:

```toml
[outputFormats.json]
weight = 1
[outputFormats.html]
weight = 2
```

Create an Atom feed in four steps:

```toml
[mediaTypes.'application/atom+xml']
suffixes = ['atom']

[outputFormats.atom]
mediaType = 'application/atom+xml'
noUgly = true

[outputs]
home = ['html', 'rss', 'atom']
section = ['html', 'rss', 'atom']
taxonomy = ['html', 'rss', 'atom']
term = ['html', 'rss', 'atom']
```

Then create the list template `layouts/list.atom.atom`, modelled on the RSS template.

Link to alternates:

```go-html-template
{{ range .AlternativeOutputFormats }}
  <link rel="{{ .Rel }}" type="{{ .MediaType.Type }}" href="{{ .Permalink | safeURL }}">
{{ end }}
```

`OutputFormats` includes the current format; `AlternativeOutputFormats` does not. Template names follow `[page kind].[output format].[suffix]`, such as `layouts/section.rss.xml`.

## Checked

2026-11-04: property list and baseName default, isPlainText effect, weight example, four-step Atom feed example, alternate-link template, OutputFormats versus AlternativeOutputFormats and template naming confirmed against the Hugo docs Output formats page. Nothing removed.

Method: documentation only; no commands were run.
