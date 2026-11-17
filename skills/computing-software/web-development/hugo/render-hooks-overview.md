---
id: computing-software.web-development.hugo.render-hooks-overview
name: render-hooks-overview
category: computing-software
field: web-development
product: hugo
tags: [render-hooks, markup-templates, layouts-markup, markdown-only, per-kind-hooks]
level: practitioner
status: docs-checked
description: "Hugo render hooks override Markdown-to-HTML conversion for blockquotes, code blocks, headings, images, links, passthrough and tables; Markdown only, with per-kind lookup."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/render-hooks/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Render hooks override how Markdown becomes HTML. Each hook is a template, one per element type. Hooks work for Markdown only; they cannot be created for other content formats (AsciiDoc, Org Mode, Pandoc, reStructuredText, HTML).

Template files, one per type:

```tree
layouts/
  └── _markup/
      ├── render-blockquote.html
      ├── render-codeblock.html
      ├── render-heading.html
      ├── render-image.html
      ├── render-link.html
      ├── render-passthrough.html
      └── render-table.html
```

The normal template lookup order applies, so you can have different hooks per page type, kind, language and output format:

```tree
layouts/
├── _markup/
│   ├── render-link.html
│   └── render-link.rss.xml
└── books/
    └── _markup/
        └── render-link.html
```

Example: without link and image hooks, this Markdown renders to plain tags.

```md
[Hugo](https://gohugo.io)

![kitten](kitten.jpg)
```

With hooks you can add `rel="external"` to the link or `width` and `height` to the image.

Each hook receives its own context, described on the per-element pages of the Hugo docs.

## Checked

2026-11-04: supported element types, Markdown-only limit, template file names, per-type/kind/language/output-format lookup and the link/image example confirmed against the Hugo docs render hooks Introduction page. Replaced a context-field list the page does not give with a pointer to the per-element pages.

Method: documentation only; no commands were run.
