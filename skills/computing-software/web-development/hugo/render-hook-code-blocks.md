---
id: computing-software.web-development.hugo.render-hook-code-blocks
name: render-hook-code-blocks
category: computing-software
field: web-development
product: hugo
tags: [render-hook-codeblock, render-codeblock, language-specific-hooks, can-highlight, info-string]
level: practitioner
status: docs-checked
description: "Write render-codeblock.html and language-specific render-codeblock-LANG.html hooks: info string attributes and options, context fields and a plain-text fallback."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/render-hooks/code-blocks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A fenced code block has a fence, an optional info string, the code and a closing fence. The first word of the info string is the language; optional attributes go in braces.

````md
```sh {class="my-class" id="my-codeblock" lineNos=inline tabWidth=2}
declare a=1
```
````

- Generic attributes (`class`, `id`) go on the surrounding HTML element. Hugo removes event attributes such as `onclick`.
- Highlighting options (`lineNos`, `tabWidth`, and `style` in an info string) drive the built-in highlighter.

Context: `Attributes`, `Inner`, `Options`, `Ordinal`, `Page`, `PageInner`, `Position` and `Type` (the language).

Default hook, `layouts/_markup/render-codeblock.html`:

```go-html-template
{{ $result := transform.HighlightCodeBlock . }}
{{ $result.Wrapped }}
```

Fall back to plain text when the language is unknown or missing:

```go-html-template
{{- $opts := dict }}
{{- if not (transform.CanHighlight .Type) }}
  {{- $opts = dict "type" "text" }}
{{- end }}
{{- $result := transform.HighlightCodeBlock . $opts }}
{{- $result.Wrapped }}
```

Language-specific hooks use `render-codeblock-<language>.html`, for example `render-codeblock-mermaid.html` or `render-codeblock-python.html`, next to the generic file. Hugo includes an embedded hook for GoAT diagrams.

## Checked

2026-11-04: info string parts, generic attribute and event-attribute handling, highlighting options, context fields, default and plain-text fallback hooks, language-specific file naming and the embedded GoAT hook confirmed against the Hugo docs Code block render hooks page. Nothing removed.

Method: documentation only; no commands were run.
