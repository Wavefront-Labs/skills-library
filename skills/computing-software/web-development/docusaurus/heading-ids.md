---
id: computing-software.web-development.docusaurus.heading-ids
name: heading-ids
category: computing-software
field: web-development
product: docusaurus
tags: [heading-ids, anchor-links, explicit-id, mdx-comment-syntax, mdx1compat]
level: practitioner
status: docs-checked
description: "Generated and explicit heading IDs in Docusaurus Markdown, the MDX versus CommonMark ID syntaxes, and avoiding invalid or colliding IDs."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-toc.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each heading has an ID, used for links: `[link](#heading-id)` in Markdown or `<Link to="#heading-id">` in JSX. By default it is generated from the heading text (`### Hello World` gets `hello-world`).

Generated IDs may look bad, and changing or translating the text changes the ID and can break links. Set an explicit ID at the end of the heading; it must start with `#` and is stripped from output:

```md
### Hello World {/* #my-explicit-id */}
### Hello World <!-- #my-explicit-id -->
### Hello World {#my-explicit-id}
```

The first is the MDX syntax, the second and third are CommonMark (classic) syntax.

For MDX files avoid `{#id}`: it is not valid MDX, and can break IDEs and linters. Docusaurus supports it only with the `markdown.mdx1Compat.headingIds` option. Prefer the comment form.

Run `write-heading-ids` to add IDs to all documents; by default it uses `classic` for CommonMark-compiled files and `mdx-comment` for MDX files, per `markdown.format`. Use `--syntax` to choose another.

Generated IDs are unique per page. With custom IDs, make each appear exactly once per page, otherwise two DOM elements share an ID (invalid HTML) and one heading becomes unlinkable.

## Checked

2026-11-04. Read in full against the Docusaurus Headings and Table of contents page (markdown-features-toc.mdx), Heading IDs section: generated ID example, explicit ID syntaxes, markdown.mdx1Compat.headingIds, write-heading-ids defaults by markdown.format and --syntax, and the colliding IDs warning all match. Nothing removed.

Method: documentation only; no commands were run.
