---
id: computing-software.web-development.hugo.content-summaries
name: content-summaries
category: computing-software
field: web-development
product: hugo
tags: [summaries, more-divider, summary-front-matter, summarylength, truncated]
level: intro
status: docs-checked
description: "Hugo content summaries: manual <!--more--> divider, summary in front matter, automatic summaries via summaryLength, precedence, and rendering with .Summary."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/summaries.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three ways to define a summary, in precedence order:

| Type | Precedence | Renders Markdown | Renders shortcodes | Wraps single lines in `<p>` |
|---|:-:|:-:|:-:|:-:|
| Manual | 1 | Yes | Yes | Yes |
| Front matter | 2 | Yes | No | No |
| Automatic | 3 | Yes | Yes | Yes |

**Manual:** put `<!--more-->` on its own line to end the summary. Hugo does not render the divider. Placing it mid-sentence is incorrect. With Org Mode content use `# more`.

```md
This is the first paragraph.

<!--more-->

This is the second paragraph.
```

**Front matter:** independent of the page content.

```toml
summary = 'This summary is independent of the content.'
```

**Automatic:** if neither exists, Hugo derives one from the `summaryLength` setting. If it would end inside a container such as a blockquote or list item, Hugo extends it to the end of that element.

Render with the `Summary` method; the docs example guards a "More ..." link with `Truncated`.

```go-html-template
{{ .Summary }}
{{ if .Truncated }}
  <a href="{{ .RelPermalink }}">More ...</a>
{{ end }}
```

For granular control use `strings.Truncate`, for example `{{ .Content | strings.Truncate 42 }}`.

## Checked

2026-11-04: precedence and comparison table, divider rules, Org Mode divider, front matter summary, summaryLength, container extension, rendering and strings.Truncate example confirmed against the Hugo docs Content summaries page. Reworded the Truncated sentence, whose meaning the page does not state.

Method: documentation only; no commands were run.
