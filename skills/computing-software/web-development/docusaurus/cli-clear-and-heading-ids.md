---
id: computing-software.web-development.docusaurus.cli-clear-and-heading-ids
name: cli-clear-and-heading-ids
category: computing-software
field: web-development
product: docusaurus
tags: [docusaurus-clear, write-heading-ids, heading-ids, cache, mdx-comment-syntax]
level: practitioner
status: docs-checked
description: "Clear generated assets and caches with docusaurus clear, and add explicit heading IDs to Markdown with write-heading-ids and its syntax, migrate and overwrite flags."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/cli.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`docusaurus clear [siteDir]` clears generated assets, caches and build artifacts. Run it before reporting bugs, after upgrading versions, or whenever the site misbehaves.

`docusaurus write-heading-ids [siteDir] [files]` adds explicit heading IDs to Markdown documents.

| Option | Default | Use |
| --- | --- | --- |
| `files` | all MD files used by plugins | restrict which files are written |
| `--syntax` | inferred | `classic` (`{#id}`) or `mdx-comment` (`{/* #id */}`) |
| `--migrate` | `false` | convert existing IDs to the target `--syntax` |
| `--overwrite` | `false` | regenerate IDs from the heading text |
| `--maintain-case` | `false` | keep heading casing instead of lowercasing |

The inferred syntax is `classic` for files compiled as CommonMark and `mdx-comment` for files compiled as MDX, following the `markdown.format` config option.

```sh
npm run docusaurus write-heading-ids -- --syntax mdx-comment
```

## Checked

2026-11-04: read the Docusaurus CLI page in full. Confirmed clear, and the write-heading-ids options, defaults and inferred syntax rule. Nothing removed.

Method: documentation only; no commands were run.
