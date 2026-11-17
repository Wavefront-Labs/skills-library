---
id: computing-software.web-development.hugo.math-in-markdown
name: math-in-markdown
category: computing-software
field: web-development
product: hugo
tags: [mathematics, latex, passthrough, mathjax, katex]
level: practitioner
status: docs-checked
description: "Render LaTeX math in Hugo Markdown with the Goldmark passthrough extension plus a MathJax or KaTeX partial, delimiters, per-page enabling and chemistry."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/mathematics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Write equations in LaTeX inside Markdown; the browser renders them with MathJax or KaTeX. Delimiter pairs decide inline versus block (display) mode. (The `transform.ToMath` function can render at build time instead; this page does not cover it.)

Setup:

1. Enable the Goldmark passthrough extension in project configuration so raw Markdown inside the delimiters is preserved. Block delimiters: `\[ \]` and `$$ $$`. Inline: `\( \)`. Omit the `inline` key to disable inline passthrough.
2. Set `math = true` under `[params]` to enable math on every page. To enable only where needed, set `math = false` there and `math = true` in the page's front matter.
3. Create `layouts/_partials/math.html` that loads MathJax (version 4 from jsDelivr) or KaTeX (version 0.18.4) and configures delimiters to match your configuration.
4. Call it from `layouts/baseof.html` inside `<head>`:

```go-html-template
{{ if .Param "math" }}
  {{ partialCached "math.html" . }}
{{ end }}
```

Notes:

- `$...$` is a common inline pair but is not enabled by default. If you add it, double-escape `$` outside math (for example `\\$2`). If you also use `$` outside math, use MathJax rather than KaTeX, due to a known KaTeX limitation.
- MathJax supports chemical equations (`\ce`, `\pu`) with no extra configuration; KaTeX needs the mhchem extension.

Example: `$$C_p[\ce{H2O(l)}] = \pu{75.3 J // mol K}$$`.

## Checked

2026-11-04. Confirmed against the Hugo docs page Mathematics in Markdown: the passthrough delimiter configuration and `inline` omission, the `math` parameter behaviour, the MathJax 4 (jsDelivr) and KaTeX 0.18.4 partials, the `partialCached` call, the `$...$` double-escape note and the KaTeX limitation, and the chemistry note on mhchem. Nothing removed.

Method: documentation only; no commands were run.
