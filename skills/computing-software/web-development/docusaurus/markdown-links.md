---
id: computing-software.web-development.docusaurus.markdown-links
name: markdown-links
category: computing-software
field: web-development
product: docusaurus
tags: [markdown-links, file-path-links, url-links, relative-links, content-root]
level: practitioner
status: docs-checked
description: "Link between Docusaurus Markdown pages with file paths or URL paths: how each resolves, the content root, portability, and the same-plugin limitation."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-links.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two link styles:

```md
- [URL path to another document](./installation)
- [file path to another document](./installation.mdx)
```

URL paths are not processed: they render directly to `<a href>` and resolve against the page's URL, not its file location.

File paths to Markdown files handled by the same plugin are converted to the target's URL (the extension is removed). Relative file paths resolve from the current file's directory:

```md title="docs/folder/doc1.md"
[document](doc2.mdx)
[in a subfolder](subfolder/doc3.mdx)
[elsewhere](../otherFolder/doc4.mdx)
```

Absolute file paths resolve from the content root (usually `docs/`, `blog/`, or a localized root). Examples from `website/docs/category/source.mdx`:

- `./target.mdx`: from `website/docs/category`.
- `../target.mdx`: from `website/docs`.
- `/target.mdx`: from the docs content root, localized docs first.
- `target.mdx`: current directory, then content roots, then site root.

`/docs/target.mdx` and `@site/docs/target.mdx` resolve from the site root but are not portable: you must update them by hand when versioning or localizing.

Why prefer file paths: links work on GitHub and in editors, slugs can change freely, editors can track moves, a versioned doc links to the same version, and relative URL links break if `trailingSlash` changes.

Limitation: file references work only when source and target are processed by the same plugin instance. Linking from a blog post to a doc needs a URL link.

## Checked

2026-11-04. Read in full against the Docusaurus Markdown links page (markdown-features-links.mdx): URL versus file paths, relative and absolute resolution examples, non-portable /docs/ and @site/ links, benefits list and the same-plugin limitation all match. Nothing removed.

Method: documentation only; no commands were run.
