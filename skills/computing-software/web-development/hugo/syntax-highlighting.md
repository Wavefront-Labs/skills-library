---
id: computing-software.web-development.hugo.syntax-highlighting
name: syntax-highlighting
category: computing-software
field: web-development
product: hugo
tags: [syntax-highlighting, fenced-code-blocks, chroma, line-numbers, hl-lines]
level: practitioner
status: docs-checked
description: "Highlight code in Hugo with fenced code blocks, the highlight shortcode or transform.Highlight: language identifiers, options such as linenos and hl_lines, escaping shortcodes."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/syntax-highlighting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three ways to highlight: the `transform.Highlight` function in templates, the `highlight` shortcode in any content format, and fenced code blocks in Markdown. In the default configuration Hugo highlights fenced code blocks.

Fence syntax:

````md
```LANG [OPTIONS]
CODE
```
````

- `LANG` is case-insensitive. Omit it or use an unsupported one and Hugo renders plain text. Fenced blocks need a known language identifier to trigger highlighting.
- Use language identifiers, not language names.
- `OPTIONS` are space- or comma-separated key-value pairs in braces. Defaults can be set in project configuration; key names are case-insensitive.

````md
```go {linenos=inline hl_lines=[3,"6-8"] style=emacs}
package main

import "fmt"
```
````

To show shortcode delimiters in documentation, escape them with comment markers inside the delimiters:

````md
```text {linenos=inline}
{{</*/* shortcode-1 */*/>}}
```
````

Configuration for these settings lives in the `markup.highlight` section; see the markup configuration skill.

## Checked

2026-11-04. Confirmed against the Hugo docs page Syntax highlighting: the three methods, the fenced block form, `LANG` case-insensitivity and plain-text fallback, the identifiers-not-names rule, option syntax and case-insensitive keys, the `linenos`, `hl_lines` and `style` example and the shortcode escaping example. Nothing removed.

Method: documentation only; no commands were run.
