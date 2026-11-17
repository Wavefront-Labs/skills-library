---
id: computing-software.software-engineering.nim.nim-doc-basics
name: nim-doc-basics
category: computing-software
field: software-engineering
product: nim
tags: [nim-doc-basics, documentation-generation, nim-doc, docgen, doc-comments, rst, markdown, html-docs, documentation, nim]
level: practitioner
status: docs-checked
description: "Generate HTML docs with nim doc: doc comments, exported symbols, --project, --outdir, --git.url, importdoc, code-block, and rst2html or md2html."
sources:
  - https://nim-lang.org/docs/docgen.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nim doc basics

Goal: browsable API docs from source comments.

- `nim doc file.nim` writes HTML; by default the output goes in a `htmldocs` directory next to the processed file. Change it with `--outdir:dir`.
- Documentation comments (`##`) are attached to declarations; only exported (`*`) symbols appear in the output.
- `nim doc --project main.nim` documents the module and the imported modules of the same Nimble package. Add `--index:on` to build the index files.
- Source links: `--git.url:<url>`, `--git.commit:<tag-or-commit>` and `--git.devel:<branch>` make "source" links point to the repository.
- `--docCmd` controls how runnable examples are run; `--docRoot` sets the root for relative paths; cross-module links use `importdoc`.
- Doc comments are reStructuredText (Markdown is supported too); code blocks use `.. code-block:: nim`.
- Standalone documents: `nim rst2html file.rst` and `nim md2html file.md`.

Gotchas:
- Unexported symbols are hidden from the output.

Verify: open the generated `htmldocs/<module>.html`.

## Checked

2026-11-03. Confirmed in the docgen and compiler pages (nim doc, default output directory, `--outdir`, exported-only, `--project`, `--git.*`, `--docCmd`, `--docRoot`, importdoc, code-block, rst2html, md2html). Removed: `--docInternal`, the hard-coded `mypkg.html` output name, and the backtick cross-link claim.
Method: documentation only; no commands were run.
