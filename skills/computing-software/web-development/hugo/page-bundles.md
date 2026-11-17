---
id: computing-software.web-development.hugo.page-bundles
name: page-bundles
category: computing-software
field: web-development
product: hugo
tags: [page-bundles, leaf-bundle, branch-bundle, index-md, headless-bundle]
level: practitioner
status: docs-checked
description: "Hugo page bundles: leaf bundles with index.md, branch bundles with _index.md, which resources each can hold, page kinds, and headless bundles."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/content-management/page-bundles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A page bundle is a directory holding content and its associated resources, reached with the `Resources` method on `Page`.

**Leaf bundle:** an `index.md` plus zero or more resources, with no descendants. It can sit at any depth in `content`, cannot contain another bundle, and is `page` kind.

```tree
content/
└── posts/
    └── my-post/
        ├── content-1.md
        ├── image-1.jpg
        └── index.md
```

**Branch bundle:** an `_index.md` plus zero or more resources, possibly with descendants including leaf and branch bundles. Top-level directories (with or without `_index.md`) and the home page are branch bundles. Kinds: `home`, `section`, `taxonomy`, `term`.

The index file extension follows the content format, such as `index.adoc` for AsciiDoc.

Resource rules:

- Branch bundle resources can be any type except `page`.
- Leaf bundle resources can be any type, including `page`.
- In a leaf bundle, `page`-type files other than the index (Markdown, HTML, AsciiDoc, Pandoc, reStructuredText, Org Mode) are only page resources and are not rendered as pages. In a branch bundle they are only content pages.

**Headless bundles** are created with build options in front matter. They are unpublished, but their content and resources can be included in other pages.

## Checked

2026-11-04: leaf and branch bundle definitions, page kinds, resource-type rules, index file extension and headless bundle statement confirmed against the Hugo docs Page bundles page. Removed a cross-reference to another skill that the page does not contain.

Method: documentation only; no commands were run.
