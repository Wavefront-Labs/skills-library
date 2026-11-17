---
id: computing-software.web-development.jekyll.kramdown-and-markdown-options
name: kramdown-and-markdown-options
category: computing-software
field: web-development
product: jekyll
tags: [kramdown, gfm-processor, coderay, commonmark, custom-markdown-processor]
level: advanced
status: docs-checked
description: "Configure Markdown in Jekyll: kramdown GFM or plain input, CodeRay highlighting, advanced kramdown options, CommonMark plugins and custom processor classes."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kramdown is the default renderer. Jekyll uses its GitHub Flavored Markdown (GFM) processor, so `input: GFM` is redundant. GFM-specific options go in the kramdown block:

```yaml
kramdown:
  gfm_quirks: [paragraph_end]
```

Switch to the plain processor with `input: Kramdown`. Any other kramdown parser needs its gem added.

CodeRay: add the `kramdown-syntax-coderay` gem (`bundle add kramdown-syntax-coderay`), then:

```yaml
kramdown:
  syntax_highlighter: coderay
  syntax_highlighter_opts:
    line_numbers: table
    bold_every: 5
```

Other kramdown options such as `header_offset` and `smart_quotes` go in the same block. Jekyll uses kramdown's HTML converter, so options meant for other converters (e.g. `remove_block_html_tags`) have no effect.

CommonMark is implemented in C and faster than Ruby kramdown, but lacks some kramdown syntax such as Block Inline Attribute Lists. Use the `jekyll-commonmark` plugin, or `jekyll-commonmark-ghpages` for the GitHub Pages flavour.

Custom processor: define a class in `Jekyll::Converters::Markdown` with `initialize(config)` and `convert(content)`, ship it in `_plugins` or a gem, then set `markdown: MyCustomProcessor`.

## Checked

2026-11-04. Confirmed against the Jekyll Markdown options doc: GFM default and redundant `input: GFM`, `gfm_quirks`, `input: Kramdown`, the CodeRay gem and `syntax_highlighter_opts` example, `header_offset` and `smart_quotes`, the unsupported-options warning, CommonMark claims and both plugins, and the custom processor class and config. Nothing removed.

Method: documentation only; no commands were run.
