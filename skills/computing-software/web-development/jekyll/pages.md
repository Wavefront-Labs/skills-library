---
id: computing-software.web-development.jekyll.pages
name: pages
category: computing-software
field: web-development
product: jekyll
tags: [pages, standalone-content, page-urls, subfolders, output-url]
level: intro
status: docs-checked
description: "Add standalone Jekyll pages as HTML or Markdown files, understand how source paths map to URLs, and when permalinks change the output folders."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/pages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pages are the basic building block for standalone, non-date-based content. Add an HTML file in the root with a suitable filename, or a `.md` file with front matter that converts to HTML on build.

```
.
├── about.md      # => http://example.com/about.html
├── index.html    # => http://example.com/
└── contact.html  # => http://example.com/contact.html
```

For many pages, use subfolders. The same subfolders appear in `_site`:

```
.
├── about.md          # => http://example.com/about.html
├── documentation
│   └── doc1.md       # => http://example.com/documentation/doc1.html
├── design
│   └── draft.md      # => http://example.com/design/draft.html
```

If a page sets a different permalink in front matter, its folder in `_site` changes accordingly. Use permalinks for full control of output URLs independent of source layout.

Page excerpts are optional: set `page_excerpts` to `true` in config (4.1.1+).

Use a page (not a collection) for content that is not date based or part of a group like staff members or recipes.

## Checked

2026-11-04. Confirmed against the Jekyll pages doc: root HTML and `.md` pages, both directory trees with their URLs, the subfolder and permalink behaviour, `page_excerpts` with the 4.1.1 badge, and the pages-versus-collections guidance. Nothing removed.

Method: documentation only; no commands were run.
