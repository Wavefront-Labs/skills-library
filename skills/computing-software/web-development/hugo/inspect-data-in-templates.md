---
id: computing-software.web-development.hugo.inspect-data-in-templates
name: inspect-data-in-templates
category: computing-software
field: web-development
product: hugo
tags: [debug-dump, printf, warnf, templates-current, troubleshooting]
level: intro
status: docs-checked
description: "Inspect values in Hugo templates with debug.Dump, printf type formatting, warnf console logging and templates.Current."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/troubleshooting/inspection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hugo has template functions for inspecting values and data structures.

- `debug.Dump` renders a full data structure as formatted output. Inside a `<pre>` tag, `{{ debug.Dump .Params }}` shows a page's front matter fields as JSON.
- `printf` shows a simple value and its type. With the format `"%[1]v (%[1]T)"`, a value of `42` renders as `42 (int)`.
- `warnf` works like `printf` but logs to the console instead of the page.
- `templates.Current` (added in v0.146.0) marks template execution boundaries or shows the template call stack.

```go-html-template
<pre>{{ debug.Dump .Params }}</pre>
{{ printf "%[1]v (%[1]T)" 42 }}
```

## Checked

2026-11-04: debug.Dump example, printf layout and output, warnf logging and templates.Current (new in 0.146.0) confirmed against the Hugo docs Data inspection page. Nothing removed.

Method: documentation only; no commands were run.
