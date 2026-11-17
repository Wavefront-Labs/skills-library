---
id: computing-software.web-development.hugo.sections
name: sections
category: computing-software
field: web-development
product: hugo
tags: [sections, subsections, list-pages, ancestors, breadcrumbs]
level: practitioner
status: docs-checked
description: "Understand Hugo sections: top-level directories or those with _index.md, list pages, templates chosen by top-level section, ancestors and descendants."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/sections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A section is a top-level directory under `content/` or any directory containing an `_index.md`. A section inside another is a subsection. Directory names become URL segments.

Sections have list pages and logical ancestors and descendants; plain directories have neither. If `articles` is a section but `articles/2022` has no `_index.md`, its list page still includes every article regardless of directory structure and `articles/2022` has no list page of its own.

By default a section's list page includes its direct children, not their descendants. To include descendants use `RegularPagesRecursive` instead of `Pages` in the section template.

Template lookup considers only the top-level section name; subsection names are ignored. In the page's example, `content/products`, `content/products/product-1` and `content/products/product-1/benefits` all use `layouts/products/section.html` and `layouts/products/page.html`. For a different template in a subsection, set `type` and/or `layout` in its front matter.

`Parent` and `Ancestors` traverse the structure. The page builds a breadcrumb partial at `layouts/_partials/breadcrumb.html` by looping:

```go-html-template
{{ range .Ancestors.Reverse }}
```

The result reads `Home » Products » Product 1 » Benefits » Benefit 1`.

## Checked

2026-11-04: section definition, list page behaviour, RegularPagesRecursive, top-level-section template lookup, type/layout override and the breadcrumb example confirmed against the Hugo docs Sections page. Nothing removed.

Method: documentation only; no commands were run.
