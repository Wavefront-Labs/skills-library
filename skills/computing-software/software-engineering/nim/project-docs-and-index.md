---
id: computing-software.software-engineering.nim.project-docs-and-index
name: project-docs-and-index
category: computing-software
field: software-engineering
product: nim
tags: [project-docs-and-index, documentation-generation, doc-project, theindex, index, github-pages, buildindex, docs-publish, nim]
level: practitioner
status: docs-checked
description: "Generate project-wide HTML docs with nim doc --project --index:on, build theindex.html with nim buildIndex, add source links with --git.url/--git.commit/--git.devel."
sources:
  - https://nim-lang.org/docs/docgen.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project-wide docs, index and theindex

Goal: publish documentation for a package.

- The documented one-liner: `nim doc --project --index:on --git.url:<url> --git.commit:<tag> --outdir:htmldocs <main_filename>.nim`. It generates HTML files, a `theindex.html` index, css and js under `htmldocs`.
- `--project` recursively documents all Nim modules imported into the input module that belong to the same Nimble package as that file. With `--project` the output replicates the project's directory structure inside `--outdir`.
- `--index:on` only creates `.idx` files; the searchable `theindex.html` comes from `nim buildIndex -o:path/to/htmldocs/theindex.html path/to/htmldocs`, which goes over all index files in that directory.
- `--git.url:<url>` adds a "See source" link under each documented item. `--git.commit` overrides the hardcoded `devel` branch (use a branch, tag or commit); `--git.devel` does the same for the Edit link.
- Importing docs across modules (`importdoc`) needs `.idx` files first: use `--index:only`, then the normal run, with the same `--outdir` for both.
- Hand-written pages use `nim rst2html` (reStructuredText) and `nim md2html` (Markdown).
- `runnableExamples` blocks are run while generating docs unless `--docCmd:skip` is given.
- Wrap the commands in a nimble task or a CI step; hosting is up to you.

Gotchas:
- Without `--outdir`, output goes to an `htmldocs` subdirectory next to the processed file.
- Use the same `--outdir` for `--index:only` and the final run.

Verify: `htmldocs/theindex.html` lists your exported symbols.

## Checked

2026-11-03. Confirmed in the docgen page and the compiler guide: command line above, `--project` semantics, `--index` vs `buildIndex`, `--git.*` switches, `--index:only` with `importdoc`, `rst2html`/`md2html` commands, `--docCmd` and `runnableExamples`. Removed: the claim that `--project` also documents stdlib modules (the page says only modules of the same Nimble package), "index is rebuilt every time", and GitHub Pages deployment steps.
Method: documentation only; no commands were run.
