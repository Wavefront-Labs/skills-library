---
id: computing-software.web-development.docusaurus.create-doc-and-tags
name: create-doc-and-tags
category: computing-software
field: web-development
product: docusaurus
tags: [create-doc, doc-front-matter, doc-tags, tags-yml, partial-pages]
level: intro
status: docs-checked
description: "Create a Docusaurus doc page, use optional front matter, ignore underscore-prefixed partials, and declare inline or predefined tags with docs/tags.yml."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/docs-create-doc.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a Markdown file such as `greeting.md` under the `docs` directory. Only h2 and h3 headings appear in the table of contents by default; this can be configured per document or in theme config.

Files prefixed with an underscore (`_`) under `docs` are partial pages and ignored by default (see importing Markdown).

Front matter is optional: Docusaurus infers all necessary metadata. Features such as tags require it.

Tags add categorisation beyond the sidebar. Define inline, or reference predefined tags from an optional tags file (usually `docs/tags.yml`):

```md title="docs/my-doc.md"
---
tags:
  - Releases
  - docusaurus
---
```

```yml title="docs/tags.yml"
docusaurus:
  label: 'Docusaurus'
  permalink: '/docusaurus'
  description: 'Docs related to the Docusaurus framework'
```

Here `docusaurus` references a predefined key and `Releases` is inline because it is absent from `tags.yml`.

Array form also works: `tags: [Demo, Getting started]`.

## Checked

2026-11-04. Read in full against the Docusaurus Create a doc page: docs directory, h2 and h3 TOC default, underscore-prefixed partial pages ignored, optional front matter, inline versus predefined tags with docs/tags.yml, and the array tag form all match. Nothing removed.

Method: documentation only; no commands were run.
